# MSRC-52108 A Case of a Win32k Race Condition 

While fuzzing Microsoft Edge i have stumbled upon a kernel BSOD. the buggy code was present in the following function: ***win32kbase!RGNMEMOBJ::vPushThreadGuardedObject***, judging from the ida xrefs to this function, we can see a window of opportunity for concurrent calls to this function:<br>

![](https://rce.wtf/images/w2k/xrefs.png)

Here is a short explanation and a little bit of debugging information:<br>

```c
win32kbase!RGNMEMOBJ::vPushThreadGuardedObject UAF due to thread management race condition.

this vulnerability is triggered when the following conditions are met:

*) require a multi core environment.

1) a Process is created with several sub-threads.
2) the main process is to be distructed triggering nt!PspTerminateAllThreads in the kernel.
3) concurrent access to the corresponding kernel structures associated with 
the sub-thread can cause an invalid pointer derefarance, 
in the kernel due to incomplete checks for the state of the thread.

then the following pattern accure:
dxgkrnl!DxgkCompositionObject::Delete -> 
	            win32kbase!CRegion::Combine -> 
		           win32kbase!RGNMEMOBJ::vPushThreadGuardedObject 
			   		^--- is accessing a free structure ..

[...]
[...]
[cut]
[...]
[...]

struct s1 {		
    struct s1* f0;
    struct s1* f8;
    struct s0* f16;
    int64_t f24;
};

struct s0 {
    signed char[48] pad48;
    struct s1* f48;
};

struct s1* g188;

int64_t PsGetThreadWin32Thread = -1;

int64_t KeEnterCriticalRegion = -1;

struct s2 {
    signed char[88] pad88;
    struct s1* f88;
};

int64_t KeLeaveCriticalRegion = -1;

/* ?vPushThreadGuardedObject@RGNMEMOBJ@@QEAAXXZ */
void vPushThreadGuardedObject_RGNMEMOBJ_QEAAXXZ(struct s0** rcx) {
    struct s1* rcx2;
    int64_t* rax3;
    struct s0* rdi4;
    struct s1* rbx5;
    struct s1* rcx6;
    struct s2* rsi7;
    struct s2** rax8;
    struct s1* rax9;

    rcx2 = g188;
    rax3 = reinterpret_cast<int64_t*>(PsGetThreadWin32Thread(rcx2));
    if (rax3 && (*rax3 && (rdi4 = *rcx, !!rdi4))) {
        rbx5 = reinterpret_cast<struct s1*>(&rdi4->f48);
        if (rbx5) {
            KeEnterCriticalRegion(rcx2);
            rcx6 = g188;
            *reinterpret_cast<int32_t*>(&rsi7) = 0;
            *reinterpret_cast<int32_t*>(reinterpret_cast<int64_t>(&rsi7) + 4) = 0;
            rax8 = reinterpret_cast<struct s2**>(PsGetThreadWin32Thread(rcx6));
            if (rax8) {
                rsi7 = *rax8;
            }
            rbx5->f16 = rdi4;
            rbx5->f24 = 0x1c010cb30;
            if (!rsi7) {
                rbx5->f8 = rbx5;
                rbx5->f0 = rbx5;
            } else {
                rcx6 = rsi7->f88;
                rax9 = reinterpret_cast<struct s1*>(&rsi7->f88);				
                if (rcx6->f8 != rax9) {					<---- we bsod here ..
                    __asm__("int 0x29");
                } else {
                    rbx5->f0 = rcx6;
                    rbx5->f8 = rax9;
                    rcx6->f8 = rbx5;
                    rax9->f0 = rbx5;
                }
            }
            KeLeaveCriticalRegion(rcx6);
        }
    }
    return;
}

[...]
[...]
[cut]
[...]
[...]


this can be triggered from within the edge sandbox.

from one memory dump:

FAULTING_IP: 
win32kbase!RGNMEMOBJ::vPushThreadGuardedObject+99
fffff1e0`56dcb449 48394108        cmp     qword ptr [rcx+8],rax

CONTEXT:  fffffb8428139850 -- (.cxr 0xfffffb8428139850)
rax=fffff1ba82653068 rbx=fffff1ba88a7bd50 rcx=0000023700000231
rdx=fffff1ba88a7bd88 rsi=fffff1ba82653010 rdi=fffff1ba88a7bd20
rip=fffff1e056dcb449 rsp=fffffb842813a240 rbp=fffffb842813a2a0
 r8=fffff1ba88a7bd20  r9=0000000000000000 r10=fffff80144027c60
r11=fffffb842813a230 r12=ffffb181b9146090 r13=fffff1ba872eabc0
r14=fffff1ba860aac30 r15=fffff1ba872eabc0
iopl=0         nv up ei ng nz na pe nc
cs=0010  ss=0018  ds=002b  es=002b  fs=0053  gs=002b             efl=00010282
win32kbase!RGNMEMOBJ::vPushThreadGuardedObject+0x99:
fffff1e0`56dcb449 48394108        cmp     qword ptr [rcx+8],rax ds:002b:00000237`00000239=????????????????


1: kd> k
 # Child-SP          RetAddr           Call Site
00 fffffb84`28138f18 fffff801`441d1e69 nt!KeBugCheckEx
01 fffffb84`28138f20 fffff801`441d12bc nt!KiBugCheckDispatch+0x69
02 fffffb84`28139060 fffff801`441c9222 nt!KiSystemServiceHandler+0x7c
03 fffffb84`281390a0 fffff801`44122240 nt!RtlpExecuteHandlerForException+0x12
04 fffffb84`281390d0 fffff801`4402fac4 nt!RtlDispatchException+0x430
05 fffffb84`28139820 fffff801`441d1f42 nt!KiDispatchException+0x144
06 fffffb84`28139ed0 fffff801`441ce268 nt!KiExceptionDispatch+0xc2
07 fffffb84`2813a0b0 fffff1e0`56dcb449 nt!KiPageFault+0x428
08 fffffb84`2813a240 fffff1e0`56dcbeda win32kbase!RGNMEMOBJ::vPushThreadGuardedObject+0x99
09 fffffb84`2813a270 fffff1e0`56dcbe19 win32kbase!CRegion::InternalCombine+0xb6
0a fffffb84`2813a2d0 fffff801`5a327831 win32kbase!CRegion::Combine+0x9
0b fffffb84`2813a300 fffff801`5a349e9d dxgkrnl!CCompositionToken::UpdateDirtyRegions+0x119
0c fffffb84`2813a350 fffff801`5a327b5a dxgkrnl!CCompositionToken::Discard+0x13dbd
0d fffffb84`2813a380 fffff801`5a337028 dxgkrnl!CCompositionToken::MarkInvalid+0x3a
0e fffffb84`2813a3b0 fffff801`5a336aa2 dxgkrnl!CCompositionToken::Delete+0x28
0f fffffb84`2813a3e0 fffff801`4460a490 dxgkrnl!DxgkCompositionObject::Delete+0x72
10 fffffb84`2813a470 fffff801`440e2039 nt!ObpRemoveObjectRoutine+0x80
11 fffffb84`2813a4d0 fffff801`44627e10 nt!ObfDereferenceObjectWithTag+0xc9
12 fffffb84`2813a510 fffff801`44684045 nt!ObCloseHandleTableEntry+0x270
13 fffffb84`2813a650 fffff801`447d0278 nt!ExSweepHandleTable+0xc5
14 fffffb84`2813a700 fffff801`4468e103 nt!PspRundownSingleProcess+0x14c594
15 fffffb84`2813a780 fffff801`4468f05c nt!PspTerminateAllThreads+0x21f
16 fffffb84`2813a7f0 fffff801`445d6f3f nt!PspTerminateProcess+0xe0
17 fffffb84`2813a830 fffff801`445eaca0 nt!PsTerminateProcess+0x2b
18 fffffb84`2813a860 fffff801`445e7565 nt!PspRemoveProcessFromJobChain+0x2a4
19 fffffb84`2813a940 fffff801`445ecec2 nt!PspTerminateProcessesJobCallback+0xa5
1a fffffb84`2813a9a0 fffff801`445ecce4 nt!PspCallJobHierarchyCallbacks+0xba
1b fffffb84`2813a9f0 fffff801`445f27c1 nt!PspEnumJobsAndProcessesInJobHierarchy+0xe0
1c fffffb84`2813aa80 fffff801`445d9965 nt!PspTerminateAllProcessesInJobHierarchy+0x5d
1d fffffb84`2813aac0 fffff801`441d1888 nt!NtTerminateJobObject+0x55
1e fffffb84`2813ab00 00007ffc`048d2d84 nt!KiSystemServiceCopyEnd+0x28

SYSTEM_SERVICE_EXCEPTION (3b)
An exception happened while executing a system service routine.
Arguments:
Arg1: 00000000c0000005, Exception code that caused the bugcheck
Arg2: fffff1e056dcb449, Address of the instruction which caused the bugcheck
Arg3: fffffb8428139850, Address of the context record for the exception that caused the bugcheck
Arg4: 0000000000000000, zero.

Debugging Details:
------------------

EXCEPTION_CODE: (NTSTATUS) 0xc0000005 - The instruction at 0x%p referenced memory at 0x%p. The memory could not be %s.

FAULTING_IP: 
win32kbase!RGNMEMOBJ::vPushThreadGuardedObject+99
fffff1e0`56dcb449 48394108        cmp     qword ptr [rcx+8],rax

CONTEXT:  fffffb8428139850 -- (.cxr 0xfffffb8428139850)
rax=fffff1ba82653068 rbx=fffff1ba88a7bd50 rcx=0000023700000231
rdx=fffff1ba88a7bd88 rsi=fffff1ba82653010 rdi=fffff1ba88a7bd20
rip=fffff1e056dcb449 rsp=fffffb842813a240 rbp=fffffb842813a2a0
 r8=fffff1ba88a7bd20  r9=0000000000000000 r10=fffff80144027c60
r11=fffffb842813a230 r12=ffffb181b9146090 r13=fffff1ba872eabc0
r14=fffff1ba860aac30 r15=fffff1ba872eabc0
iopl=0         nv up ei ng nz na pe nc
cs=0010  ss=0018  ds=002b  es=002b  fs=0053  gs=002b             efl=00010282
win32kbase!RGNMEMOBJ::vPushThreadGuardedObject+0x99:
fffff1e0`56dcb449 48394108        cmp     qword ptr [rcx+8],rax ds:002b:00000237`00000239=????????????????
Resetting default scope

==============================
redacted
==============================

DEFAULT_BUCKET_ID:  CODE_CORRUPTION

BUGCHECK_STR:  0x3B

PROCESS_NAME:  MicrosoftEdgeCP.exe <---------------------------------------------------------------------

CURRENT_IRQL:  0

ANALYSIS_SESSION_TIME:  04-26-2019 07:05:14.0763

ANALYSIS_VERSION: 10.0.16299.15 amd64fre

LAST_CONTROL_TRANSFER:  from fffff1e056dcbeda to fffff1e056dcb449

CHKIMG_EXTENSION: !chkimg -lo 50 -d !win32kfull
    fffff1e056a1fccf - win32kfull!xxxSendMessageToClient+10f
	[ 00:90 ]
    fffff1e056a1fd3c-fffff1e056a1fd3d  2 bytes - win32kfull!xxxSendMessageToClient+17c (+0x6d)
	[ 48 ff:4c 8b ]
    fffff1e056a1fd43-fffff1e056a1fd46  4 bytes - win32kfull!xxxSendMessageToClient+183 (+0x07)
	[ 0f 1f 44 00:e8 d8 16 37 ]
    fffff1e056a1fd68-fffff1e056a1fd69  2 bytes - win32kfull!xxxSendMessageToClient+1a8 (+0x25)
	[ 48 ff:4c 8b ]
    fffff1e056a1fd6f-fffff1e056a1fd72  4 bytes - win32kfull!xxxSendMessageToClient+1af (+0x07)
	[ 0f 1f 44 00:e8 ac 16 37 ]
    fffff1e056a1fd85-fffff1e056a1fd86  2 bytes - win32kfull!xxxSendMessageToClient+1c5 (+0x16)
	[ 48 ff:4c 8b ]
    fffff1e056a1fd8c-fffff1e056a1fd8f  4 bytes - win32kfull!xxxSendMessageToClient+1cc (+0x07)
	[ 0f 1f 44 00:e8 8f 16 37 ]
    fffff1e056a24152-fffff1e056a24153  2 bytes - win32kfull!xxxReceiveMessage+366 (+0x43c6)
	[ 48 ff:4c 8b ]
    fffff1e056a24159-fffff1e056a2415c  4 bytes - win32kfull!xxxReceiveMessage+36d (+0x07)
	[ 0f 1f 44 00:e8 c2 d2 36 ]
    fffff1e056a24209-fffff1e056a2420a  2 bytes - win32kfull!xxxReceiveMessage+41d (+0xb0)
	[ 48 ff:4c 8b ]
    fffff1e056a24210-fffff1e056a24213  4 bytes - win32kfull!xxxReceiveMessage+424 (+0x07)
	[ 0f 1f 44 00:e8 0b d2 36 ]
    fffff1e056a24864-fffff1e056a24865  2 bytes - win32kfull!NtUserPeekMessage+184 (+0x654)
	[ 48 ff:4c 8b ]
    fffff1e056a2486b-fffff1e056a2486e  4 bytes - win32kfull!NtUserPeekMessage+18b (+0x07)
	[ 0f 1f 44 00:e8 b0 cb 36 ]
    fffff1e056a24906-fffff1e056a24907  2 bytes - win32kfull!xxxRealInternalGetMessage+76 (+0x9b)
	[ 48 ff:4c 8b ]
    fffff1e056a2490d-fffff1e056a24910  4 bytes - win32kfull!xxxRealInternalGetMessage+7d (+0x07)
	[ 0f 1f 44 00:e8 0e cb 36 ]
    fffff1e056a25237-fffff1e056a25238  2 bytes - win32kfull!xxxRealInternalGetMessage+9a7 (+0x92a)
	[ 48 ff:4c 8b ]
    fffff1e056a2523e-fffff1e056a25241  4 bytes - win32kfull!xxxRealInternalGetMessage+9ae (+0x07)
	[ 0f 1f 44 00:e8 dd c1 36 ]
    fffff1e056a2528c-fffff1e056a2528d  2 bytes - win32kfull!xxxRealInternalGetMessage+9fc (+0x4e)
	[ 48 ff:4c 8b ]
    fffff1e056a25293-fffff1e056a25296  4 bytes - win32kfull!xxxRealInternalGetMessage+a03 (+0x07)
	[ 0f 1f 44 00:e8 88 c1 36 ]
    fffff1e056afa440-fffff1e056afa441  2 bytes - win32kfull!SfnPOWERBROADCAST+2f0 (+0xd51ad)
	[ 48 ff:4c 8b ]
    fffff1e056afa447-fffff1e056afa44a  4 bytes - win32kfull!SfnPOWERBROADCAST+2f7 (+0x07)
	[ 0f 1f 44 00:e8 d4 6f 29 ]
    fffff1e056afa460-fffff1e056afa461  2 bytes - win32kfull!SfnPOWERBROADCAST+310 (+0x19)
	[ 48 ff:4c 8b ]
    fffff1e056afa467-fffff1e056afa46a  4 bytes - win32kfull!SfnPOWERBROADCAST+317 (+0x07)
	[ 0f 1f 44 00:e8 b4 6f 29 ]
67 errors : !win32kfull (fffff1e056a1fccf-fffff1e056afa46a)

MODULE_NAME: memory_corruption

IMAGE_NAME:  memory_corruption

FOLLOWUP_NAME:  memory_corruption

DEBUG_FLR_IMAGE_TIMESTAMP:  0

MEMORY_CORRUPTOR:  LARGE

STACK_COMMAND:  .cxr 0xfffffb8428139850 ; kb

FAILURE_BUCKET_ID:  MEMORY_CORRUPTION_LARGE

BUCKET_ID:  MEMORY_CORRUPTION_LARGE

PRIMARY_PROBLEM_CLASS:  MEMORY_CORRUPTION_LARGE

ANALYSIS_SOURCE:  KM

FAILURE_ID_HASH_STRING:  km:memory_corruption_large

Followup:     memory_corruption
---------

1: kd> k
 # Child-SP          RetAddr           Call Site
00 fffffb84`28138f18 fffff801`441d1e69 nt!KeBugCheckEx
01 fffffb84`28138f20 fffff801`441d12bc nt!KiBugCheckDispatch+0x69
02 fffffb84`28139060 fffff801`441c9222 nt!KiSystemServiceHandler+0x7c
03 fffffb84`281390a0 fffff801`44122240 nt!RtlpExecuteHandlerForException+0x12
04 fffffb84`281390d0 fffff801`4402fac4 nt!RtlDispatchException+0x430
05 fffffb84`28139820 fffff801`441d1f42 nt!KiDispatchException+0x144
06 fffffb84`28139ed0 fffff801`441ce268 nt!KiExceptionDispatch+0xc2
07 fffffb84`2813a0b0 fffff1e0`56dcb449 nt!KiPageFault+0x428
08 fffffb84`2813a240 fffff1e0`56dcbeda win32kbase!RGNMEMOBJ::vPushThreadGuardedObject+0x99
09 fffffb84`2813a270 fffff1e0`56dcbe19 win32kbase!CRegion::InternalCombine+0xb6
0a fffffb84`2813a2d0 fffff801`5a327831 win32kbase!CRegion::Combine+0x9
0b fffffb84`2813a300 fffff801`5a349e9d dxgkrnl!CCompositionToken::UpdateDirtyRegions+0x119
0c fffffb84`2813a350 fffff801`5a327b5a dxgkrnl!CCompositionToken::Discard+0x13dbd
0d fffffb84`2813a380 fffff801`5a337028 dxgkrnl!CCompositionToken::MarkInvalid+0x3a
0e fffffb84`2813a3b0 fffff801`5a336aa2 dxgkrnl!CCompositionToken::Delete+0x28
0f fffffb84`2813a3e0 fffff801`4460a490 dxgkrnl!DxgkCompositionObject::Delete+0x72
10 fffffb84`2813a470 fffff801`440e2039 nt!ObpRemoveObjectRoutine+0x80
11 fffffb84`2813a4d0 fffff801`44627e10 nt!ObfDereferenceObjectWithTag+0xc9
12 fffffb84`2813a510 fffff801`44684045 nt!ObCloseHandleTableEntry+0x270
13 fffffb84`2813a650 fffff801`447d0278 nt!ExSweepHandleTable+0xc5
14 fffffb84`2813a700 fffff801`4468e103 nt!PspRundownSingleProcess+0x14c594
15 fffffb84`2813a780 fffff801`4468f05c nt!PspTerminateAllThreads+0x21f
16 fffffb84`2813a7f0 fffff801`445d6f3f nt!PspTerminateProcess+0xe0
17 fffffb84`2813a830 fffff801`445eaca0 nt!PsTerminateProcess+0x2b
18 fffffb84`2813a860 fffff801`445e7565 nt!PspRemoveProcessFromJobChain+0x2a4
19 fffffb84`2813a940 fffff801`445ecec2 nt!PspTerminateProcessesJobCallback+0xa5
1a fffffb84`2813a9a0 fffff801`445ecce4 nt!PspCallJobHierarchyCallbacks+0xba
1b fffffb84`2813a9f0 fffff801`445f27c1 nt!PspEnumJobsAndProcessesInJobHierarchy+0xe0
1c fffffb84`2813aa80 fffff801`445d9965 nt!PspTerminateAllProcessesInJobHierarchy+0x5d
1d fffffb84`2813aac0 fffff801`441d1888 nt!NtTerminateJobObject+0x55
1e fffffb84`2813ab00 00007ffc`048d2d84 nt!KiSystemServiceCopyEnd+0x28
1f 000000ac`fab7f2e8 00000000`00000000 0x00007ffc`048d2d84
```

***Timeline***<br>
This case was submitted to MSRC at 05/02/2019.<br>
in a replay to the original submission email thread i have provided my pgp key.<br>
after the corresponding patch tuesday i still didn't got a replay from MSRC about a case being opened,<br>
so i asked them about a status update.<br>
the 'case manager' notified me that he was thinking that i only wanted to share my pgp,<br>
and didn't read the original massage.<br>
at that point the vulnerabilty was patched so i asked him to close the case.<br>
judging from the acknowledgments the only win32k CVE for that patch is <a href="https://portal.msrc.microsoft.com/en-us/security-guidance/advisory/CVE-2019-0892">CVE-2019-0892</a> but i guess we can never know for sure..<br><br>

nevertheless the following patch analysis can explain the root cause of this bug and how it was fixed,
if we would decompile the relevent function before and after the patch we can find:<br>

![](https://rce.wtf/images/w2k/diff.png)

and this is the corresponding code before the patch:<br>

```c
void __fastcall RGNMEMOBJ::vPushThreadGuardedObject(RGNMEMOBJ *this)
{
  RGNMEMOBJ *v1; // rdi
  _QWORD *v2; // rax
  _QWORD *v3; // rdi
  _QWORD *v4; // rbx
  __int64 v5; // rsi
  __int64 *v6; // rax
  __int64 v7; // rcx
  _QWORD *v8; // rax

  v1 = this;
  v2 = (_QWORD *)PsGetThreadWin32Thread(__readgsqword(0x188u));	<--- get the Thread pointer from the
  								  RGNMEMOBJ passed to the function.
if ( v2 )
  {
    if ( *v2 )
    {
      v3 = *(_QWORD **)v1;				<-- cast pointers to structures..
      if ( v3 )
      {
        v4 = v3 + 6;
        if ( v3 != (_QWORD *)-48i64 )
        {
          KeEnterCriticalRegion();
	  
          v5 = 0i64;   <--- if this value (0 for int64..) remains, then note this as failure,
	                    and the condition noted in [1] would be false..
	  
          v6 = (__int64 *)PsGetThreadWin32Thread(__readgsqword(0x188u));     
          if ( v6 )
            v5 = *v6;
          v3[8] = v3;
          v3[9] = sub_1C010CB30;
	  
          if ( v5 ) <-------------------- [1]
          {
            v7 = *(_QWORD *)(v5 + 88);
            v8 = (_QWORD *)(v5 + 88);
            if ( *(_QWORD *)(v7 + 8) != v5 + 88 ) <--- casting this pointer
	    					     would result with an invalid 
						     pointer derefarance as this structure
						     now points to unmapped memory due to the thread
						     current state.
	    __fastfail(3u);
            *v4 = v7;
            v3[7] = v8;
            *(_QWORD *)(v7 + 8) = v4;
            *v8 = v4;
          }
          else
          {
            v3[7] = v3 + 6;
            *v4 = v4;
          }
          KeLeaveCriticalRegion();
        }
      }
    }
  }
}
```


The main diff from the patched version is that instead of fetching pointers with<br>
PsGetThreadWin32Thread there is now a wrapper function:

```
v2 = (_QWORD *)PsGetThreadWin32Thread(__readgsqword(0x188u));
```

Is now using:

```
if ( sub_1C001F000(__readgsqword(0x188u)) )
```

lets look at the wrapper function:


```c
__int64 __fastcall sub_1C001F000(__int64 a1)
{
  __int64 v1; // rdi
  __int64 v2; // rbx
  __int64 *v3; // rax

  v1 = a1;
  v2 = 0i64;
  if ( !(unsigned int)sub_1C00B4B60() )
  {
    v3 = (__int64 *)PsGetThreadWin32Thread(v1);
    if ( v3 )
      v2 = *v3;
  }
  return v2;
}
```

this is again just a wrapper around another function, so lets follow along:

```c
_BOOL8 sub_1C00B4B60()
{
  __int64 v0; // rax
  int v1; // ebx
  __int64 v2; // rax
  _BOOL8 result; // rax

  result = 0;
  if ( (unsigned __int8)KeIsAttachedProcess() )
  {
    v0 = PsGetCurrentProcess();
    v1 = PsGetProcessSessionIdEx(v0);
    v2 = PsGetCurrentThreadProcess();
    if ( v1 != (unsigned int)PsGetProcessSessionIdEx(v2) )
      result = 1;
  }
  return result;
}
```

the first obvious check to be added (no metter how deep is the new call stack,<br>
is the KeIsAttachedProcess function call. from reactos we find:<br>

```c
BOOLEAN
 NTAPI
 KeIsAttachedProcess(VOID)
 {
     /* Return the APC State */
     return KeGetCurrentThread()->ApcStateIndex;
 }
```

So we basicaly now check the state of the thread, and if this is found not to be a valid thread,
then the function won't access the raw pointers. i think we can claim that this bug was indeed properly fixed.


# Final Notes:
as a variant analysis prototype (to search for similar vulnerable patterns), one can look for direct calls to PsGetThreadWin32Thread, and later casting without further checks..<br>
this is very much alike the second bug discussed here: <a href="https://rce.wtf/2019/05/28/Safari.html">#</a>.<br>
it looks like win32k is always a good attack surface for EOP, and i am surprised that fuzzers like <a href="https://github.com/compsec-snu/razzer">razzer</a>, are not yet implemented for this complex driver.<br>



