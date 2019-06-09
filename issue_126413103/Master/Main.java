package com.media.automation.testing;



import java.net.MalformedURLException;
import java.net.URL;
import java.util.concurrent.ThreadLocalRandom;
 
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.DriverCommand;
import org.openqa.selenium.remote.RemoteExecuteMethod;
import org.openqa.selenium.By;
import org.openqa.selenium.Dimension;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.Platform;
import org.openqa.selenium.WebDriverException;
import org.openqa.selenium.WebElement;

import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.remote.CapabilityType;

import io.appium.java_client.MultiTouchAction;
import io.appium.java_client.TouchAction;
import org.openqa.selenium.Dimension;
 
import java.time.Duration;
 
import static io.appium.java_client.touch.TapOptions.tapOptions;
import static io.appium.java_client.touch.WaitOptions.waitOptions;
import static io.appium.java_client.touch.offset.ElementOption.element;
import static io.appium.java_client.touch.offset.PointOption.point;
import static java.time.Duration.ofMillis;
import static java.time.Duration.ofSeconds;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;

import io.appium.java_client.ios.IOSDriver;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileElement;
import io.appium.java_client.TouchAction;
import io.appium.java_client.ios.IOSElement;
import io.appium.java_client.remote.MobileCapabilityType;
 
public class Main {

	

	public static String SearchTargets[];
	
	public static String BullshitWebsites[] = {
			"https://facebook.com","https://baidu.com",
			"https://wikipedia.org","https://twitter.com","https://ebay.com/","https://yahoo.com",
			"https://www.twitch.tv/","https://www.amazon.com/","https://netflix.com","https://pornhub.com",
			"https://bit.ly","https://ow.ly","http://www.whatsmyip.org/","https://thepiratebay.org/",
			"https://youtu.be","https://www.dropbox.com","https://github.com/","https://yandex.com/","https://tutanota.com/",
			"https://ok.ru/","https://123movieshub.sc","https://ping.eu/","https://tinyurl.com/","https://www.godaddy.com",
			"https://www.hidemyass.com","https://stackoverflow.com","https://www.quora.com/","https://www.tumblr.com/",
			"https://www.youporn.com/","https://www.redtube.com/","https://hqporner.com/",
			"https://www.patreon.com/","https://vimeo.com/","https://www.pinterest.com/",
			"https://www.shodan.io/","https://torrentfreak.com","https://www.lifewire.com",
			"https://www.imdb.com/","https://www.rottentomatoes.com/","http://pangu.io/","https://www.apple.com/",
			"https://www.microsoft.com/en-us/", "https://instagram.com","https://bankofamerica.com","https://protonmail.com/",
			"https://www.coindesk.com/price/bitcoin","https://www.wired.com",
			"https://www.nytimes.com/","https://www.coinbase.com/","https://www.reuters.com","https://www.reuters.com"
			
			
	};
	
	public static List<String> SeTargets = new ArrayList<String>();
	
    @SuppressWarnings("rawtypes")
	public static AppiumDriver drv;
	@SuppressWarnings("rawtypes")
	public static AppiumDriver drv2;
	@SuppressWarnings("rawtypes")
	public static AppiumDriver Safari;
	@SuppressWarnings("rawtypes")
	public static AppiumDriver gdrv;
	public static URL url;
	public static int OSVersion;
	public static String udid;
	public static String URL_STRING;
	public static String wdurl;
	public static String dname;
	public static String apurl;
	public static String port;
	public static String Tar;
	public static int gg = 0;
	public static String tfile = "";
	public static String TCI[];
	public static String rq[];
	public static int mode = 1;
	public static Boolean clickNormalLinks = false;
	public static Boolean cip = true;
	public static Boolean debug = false;
	
	
	
	public static void shuffleArray(List<String> a) {
        int n = a.size();
        Random random = new Random();
        random.nextInt();
        for (int i = 0; i < n; i++) {
            int change = i + random.nextInt(n - i);
            swap(a, i, change);
        }
    }
	
	
	private static void swap(List<String> a, int i, int change) {
        String helper = a.get(i);
        a.set(i, a.get(change));
        a.set(change ,helper);
    }
		
	
	public static String loadRQ( String raw ) throws IOException {
		
		int sz = 1;
		
		FileInputStream fstream = new FileInputStream(raw);
		BufferedReader br = new BufferedReader(new InputStreamReader(fstream));

		String strLine;

		while ((strLine = br.readLine()) != null)   {
			
			if ((strLine!="")&&(strLine!="\n")) {

			sz+=1;}
		}

		fstream.close();
	
		rq = new String[sz];
	
		FileInputStream fs = new FileInputStream(raw);
		BufferedReader rl = new BufferedReader(new InputStreamReader(fs));
	
		int j = 0;

		String l;

		while ((l = rl.readLine()) != null)   {
			
			if ((l!="")&&(l!="\n")) {
		
			rq[j] = l;
			j++;}
		}

		fs.close();
		
		
		
		return "";
		
		
	}
	
	
	public static void loadTci(String path) throws IOException {
		
		if ((path == "")||!(path=="")) {
		
			int sz = 1;
		
			FileInputStream fstream = new FileInputStream(path);
			BufferedReader br = new BufferedReader(new InputStreamReader(fstream));

			String strLine;

			while ((strLine = br.readLine()) != null)   {
				
				if ((strLine!="")&&(strLine!="\n")) {

					sz+=1;
				}
			}

			fstream.close();
		
			TCI = new String[sz];
		
			FileInputStream fs = new FileInputStream(path);
			BufferedReader rl = new BufferedReader(new InputStreamReader(fs));
		
			int j = 0;

			String l;

			while ((l = rl.readLine()) != null)   {
				
				if ((l!="")&&(l!="\n")) {
			
					TCI[j] = l;
					j++;
				}
			}

			fs.close();
		}
		

		
		
	}
	
	
	public static void loadTargets() throws IOException {
		
		
		String RandomShit[] = {
				"&cr=countryUS",
				"&lr=lang_EN",
				"&hl=EN",
				"&safe=strict"
			};
		
		String abspath = System.getProperty("user.dir") + "/dict/locations.txt";
		
		loadTci(abspath);
		
		String absrq = System.getProperty("user.dir") + "/dict/search.txt";
		loadRQ(absrq);
		
		
		
		for (int i = 0; i < rq.length; i ++) {
			
			if (rq[i]==null) {continue;}
			
			for ( int j = 0; j < TCI.length; j ++) {
				
				if (rq[i].contains("#")) {
					
					
					if (TCI[j]==null) {continue;}
					
					
					
					String curr = rq[i].replaceAll(" ", "%20");
					String place = TCI[j].split(" ")[0];
				
					if (curr.toLowerCase().contains(place.toLowerCase())) {
						
						for (int ou=0;ou<10;ou++) {
						
							Random r = new Random();
							int rr = r.nextInt((8) + 1);
							String rn = String.valueOf(rr);
					
							String QUrl = "https://www.google.com/search?q=" + 
									curr.toLowerCase().replaceAll("#", "").replaceAll(place.toLowerCase(), "");
							String tci = TCI[j].split(" ")[1] + rn;
							String uule = TCI[j].split(" ")[2];
							String Crd = tci + uule;
							
							
							List<String> epiloge = new ArrayList<String>();
							epiloge.add(Crd);
							
							for (int k = 0; k < RandomShit.length; k ++) {
								
								Random rd = new Random();
								int rru = rd.nextInt((10) + 1);
								
								if ((rru & 1) == 0) {
									
									epiloge.add(RandomShit[k]);
									
								}
								
							}
							
							shuffleArray(epiloge);
							
							for (int t = 0; t < epiloge.size(); t ++) {
								
								QUrl += epiloge.get(t);
								
								
							}
							
							
							SeTargets.add(QUrl);
					}
					 		
					 		break;
							
					
					}
					
				}
				
				else {
					
					if (TCI[j]==null) {continue;}
				
					String curr = rq[i].replaceAll(" ", "%20");
					String place = TCI[j].split(" ")[0];
				
					if (curr.toLowerCase().contains(place.toLowerCase())) {
						
						for (int ou=0;ou<10;ou++) {
						
							Random r = new Random();
							int rr = r.nextInt((8) + 1);
							String rn = String.valueOf(rr);
					
							String QUrl = "https://www.google.com/search?q=" + curr;
							String tci = TCI[j].split(" ")[1] + rn;
							String uule = TCI[j].split(" ")[2];
							String Crd = tci + uule;
							
							
							List<String> epiloge = new ArrayList<String>();
							epiloge.add(Crd);
							
							for (int k = 0; k < RandomShit.length; k ++) {
								
								Random rd = new Random();
								int rru = rd.nextInt((10) + 1);
								
								if ((rru & 1) == 0) {
									
									epiloge.add(RandomShit[k]);
									
								}
								
							}
							
							shuffleArray(epiloge);
							
							for (int t = 0; t < epiloge.size(); t ++) {
								
								QUrl += epiloge.get(t);
								
								
							}
							
							
							// System.out.println(QUrl);
							
							
							SeTargets.add(QUrl);}
					 		
					 		break;
							
					
					}
				
				}
				
			}
			
			
		}		
			
}
		
	
	public static void Argp(String[] args) {
		
		
		
		if (args.length==0) {
			
			OutPut(9);
			
		}
		
		else if (args.length<7) {
			
			for (String s1: args)
	        {
	          if (s1.contains("-help")) {
	        	  OutPut(13);
	          }
	        }
			
			OutPut(9);
			
		}
		
		else if ((7<=args.length)){
			for (String s1: args)
	        {
	          if (s1.contains("-help")) {
	        	  OutPut(13);
	          }
	        }
			
			Boolean g = false;
			
			// java -jar runner.jar -udid=<UDID> -wdurl=<URL> -osv=<os version> -dname=<device name> -apurl=<apurl>
			
			for (String s1: args)
	        {
	          if (s1.contains("-help")) {
	        	  OutPut(13);
	          }
	          g = false;
	        }
			
			for (String s1: args)
	        {
	          if (s1.contains("-wdurl=")) {
	        	  g = true;
	        	  wdurl = s1.replace("-wdurl=", "");
	        	  break;
	          }
	          g = false;
	        }
			
			for (String s1: args)
	        {
	          if (s1.contains("-udid=")) {
	        	  g = true;
	        	  udid = s1.replace("-udid=", "");
	        	  break;
	          }
	          g = false;
	        }
			
			for (String s1: args)
	        {
	          if (s1.contains("-osv=")) {
	        	  g = true;
	        	  OSVersion =  Integer.parseInt(s1.replace("-osv=", ""));
	        	  break;
	          }
	          g = false;
	        }
			
			for (String s1: args)
	        {
	          if (s1.contains("-apurl=")) {
	        	  g = true;
	        	  apurl = s1.replace("-apurl=", "");
	        	  break;
	          }
	          g = false;
	        } 
			
			for (String s1: args)
	        {
	          if (s1.contains("-dname=")) {
	        	  g = true;
	        	  dname = s1.replace("-dname=", "");
	        	  break;
	          }
	          g = false;
	        } 
			
			for (String s1: args)
	        {
	          if (s1.contains("-port=")) {
	        	  g = true;
	        	  port = s1.replace("-port=", "");
	        	  break;
	          }
	          g = false;
	        } 
			
			for (String s1: args)
	        {
	          if (s1.contains("-tar=")) {
	        	  g = true;
	        	  Tar = s1.replace("-tar=", "");
	        	  break;
	          }
	          g = false;
	        }
			
			for (String s1: args)
	        {
	          if (s1.contains("-tfile=")) {
	        	  tfile = s1.replace("-tfile=", "");
	        	  break;
	          }
	        }
			
			for (String s1: args)
	        {
	          if (s1.contains("-mode=")) {
	        	  mode = Integer.parseInt(s1.replace("-mode=", ""));
	        	  break;
	          }
	        }
			for (String s1: args)
	        {
	          if (s1.contains("-clicknormallinks=true")) {
	        	  clickNormalLinks = true;
	        	  break;
	          }
	        }
			
			for (String s1: args)
	        {
	          if (s1.contains("-changeip=false")) {
	        	  cip = false;
	        	  break;
	          }
	        }
			
			if (g==false) {OutPut(9);}
			else{return;}
			
			
		}
			
		
		
		
	}
	
	
	private static void OutPut(int y) {
		
		if (y==13) {
			
			
			System.exit(0);
			
			
		}
		
		else if (y==9) {
			

			System.exit(0);
			
		}
		
		System.exit(0);
		
	}

	
	@SuppressWarnings("rawtypes")
	public static void main(
			String[] args
			) 
	{
		
		int fr = 0;
		
		Argp(args);
		
		try {
			loadTargets();
		} catch (IOException e2) {
			e2.printStackTrace();
		}
		

		
		
		try {
			if(cip) {
			ChangeIP(true);
			Thread.sleep(5000);}
		} catch (MalformedURLException e1) {
			
		} catch (InterruptedException err) {
			
		} catch (Exception err4) {
			
			System.out.print(err4);
			System.exit(-1);
			
		}
		
		
		try {
			ClearSafariData(fr);
			fr += 1;
			Thread.sleep(5000);
		} catch (MalformedURLException e1) {
			
		} catch (InterruptedException err) {
			
		} catch (Exception err4) {
			
			System.out.print(err4);
			System.exit(-1);
			
		}
		
		int h = 0;
		
		
		
		while (true) {
						
			  URL_STRING = apurl + "/wd/hub";

		      
		
			try {
				if (h==0) {
					DesiredCapabilities caps = new DesiredCapabilities();

					caps.setCapability("browserName", "Safari");
					caps.setCapability("user", "root");
					caps.setCapability("password", "alpine");
					caps.setCapability("deviceName", dname);
					caps.setCapability("platformName", "iOS");
					caps.setCapability("udid", udid); 
					caps.setCapability("automationName", "XCUITest");
					caps.setCapability("webDriverAgentUrl", wdurl);
					//caps.setCapability("nativeWebTap", "true");
					//caps.setCapability("autoDismissAlerts", "true");
					caps.setCapability("webkitResponseTimeout", 80000);
				
					Random rf = new Random();
					int rrj = rf.nextInt((BullshitWebsites.length - 1) + 1) + 0;
					String current = BullshitWebsites[rrj];
				
					caps.setCapability("safariInitialUrl", current); 
					caps.setCapability("noReset", "true"); 
					caps.setCapability("newCommandTimeout", "0");
					
					url = new URL(URL_STRING);
					Safari = new AppiumDriver(url, caps);
					//Safari.context("NATIVE_APP");
								
					
					
				}
				
				try {run(h);}catch (MalformedURLException e) {
					//e.printStackTrace();
				}
				
				h =1;
				
				
				
			} catch (MalformedURLException e) {
				System.out.println("\n\n");
				System.out.println(e);
				System.out.println("\n\n");
				e.printStackTrace();
			}
			
			try {
				ClearSafariData(23);
				Thread.sleep(3);
				if (cip) {
				ChangeIP(false);}
				Thread.sleep(3);
				
			}catch (Exception e) {
				continue;
				
			}			
		}
	}
	
	private static void run(int f) throws MalformedURLException{
			
		      
		      try {Thread.sleep(7000);}catch(Exception e) {}
		      String targets =  getSe();
		      String burl = targets;
			 
			 
			 if (f!=0) {
				 Safari.launchApp();
				 
				 
			 }
			 
			 try {Thread.sleep(5000);}catch(Exception e) {}
			 
				 
				 
				 Random rk = new Random();
				 int rrk = rk.nextInt((4 - 1) + 1) + 1;
				 System.out.println(rrk);
			 


				 
				 for (int y = 0; y <= 3; y++) {
					 
					 Random rf = new Random();
					 int rrj = rf.nextInt((BullshitWebsites.length - 1) + 1) + 0;
					 String current = BullshitWebsites[rrj];
					 
					 try {Thread.sleep(12000);}catch(Exception e) {}
					 
					 Safari.get(current);

					 Safari.manage().timeouts().implicitlyWait(15, TimeUnit.SECONDS);
				 
			 }
			 
			 
			 
			 try {Thread.sleep(5000);}catch(Exception e) {} 
			 Safari.get(burl);
			 Safari.manage().timeouts().implicitlyWait(15, TimeUnit.SECONDS);
		      
		      String Target = Tar;
		      
		      Boolean b = ProcessWebPage(Safari,Target,"down");
		      
		      if (b) {
		    	  
		    	  try {
		    		  String absp = System.getProperty("user.dir") + "/dict/log.txt";
		    		    PrintWriter out = new PrintWriter(new BufferedWriter(
		    		    		new FileWriter(absp, true)));
		    		    out.println(burl);
		    		    out.close();
		    		} catch (IOException e) {

		    		}
		      }
			  				  					  			  	  
		
	}

	
	private static String getSe() {
		
		Random r = new Random();
		int rr = r.nextInt((SeTargets.size() - 1) + 1) + 0;
		return SeTargets.get(rr);
		
	}
	
	
	private static boolean DissmissAlert (
			@SuppressWarnings("rawtypes") 
			AppiumDriver driver) {
		
		
		Map<String, Object> params = new HashMap<String, Object>();
        params.put("action", "dismiss");
        driver.executeScript("mobile:alert", params);

        return true;

        
    }
	
	
	@SuppressWarnings("rawtypes")
	private static void ChangeIP(boolean frstrun) throws MalformedURLException {
		
		if (frstrun) {
		
		URL URL;
		final String U_S = apurl + "/wd/hub";
	    URL = new URL(U_S);
		String browserName = "mobileOS";
		DesiredCapabilities cap = new DesiredCapabilities(browserName, "", Platform.ANY);

		cap.setCapability("user", "");
		cap.setCapability("password", "");
		cap.setCapability("deviceName", dname);
		cap.setCapability("platformName", "iOS");
		cap.setCapability("udid", udid); 
		cap.setCapability("automationName", "XCUITest");
		cap.setCapability("webDriverAgentUrl", wdurl);
		cap.setCapability("app", "com.nordvpn.NordVPN");
		cap.setCapability("noReset", "true");
		cap.setCapability("newCommandTimeout", "0");


		drv2 = new AppiumDriver(URL, cap);
		
		}
		
		else {
			
			
			drv2.launchApp();
		}
		
		
		try {
		
			drv2.findElementByAccessibilityId("Disconnect").click();
			try {
				Thread.sleep(1000);}
				catch(Exception e) {}
			
		} catch (Exception e) {
			System.out.print(e);
			}
		
		try {
			
			drv2.findElementByAccessibilityId("Quick Connect").click();
			try {
				Thread.sleep(10000);}
				catch(Exception e) {}
			
		} catch (Exception e) {

			System.out.print(e);
			}
		
		
		
		try {
			Thread.sleep(22000);
		} catch (InterruptedException e) {

			//e.printStackTrace();
		}
		
	}
	

	@SuppressWarnings("rawtypes")
	private static void ClearSafariData(int frstr) throws MalformedURLException {
		
		if (frstr==0) {
			
			try {
				Thread.sleep(2000);
			} catch (Exception er) {}
		
			URL URL;
			final String U_S = apurl + "/wd/hub";
			URL = new URL(U_S);
			String browserName = "mobileOS";
			DesiredCapabilities cap = new DesiredCapabilities(browserName, "", Platform.ANY);

			//cap.setCapability("user", "root");
			//cap.setCapability("password", "alpine");
			//
			//"platformName": "iOS",
		    //"platformVersion": "11.0",
			//
			//
			
			cap.setCapability("deviceName", dname);
			cap.setCapability("platformName", "iOS");
			cap.setCapability("udid", udid); 
			cap.setCapability("automationName", "XCUITest");
			cap.setCapability("webDriverAgentUrl", wdurl);
			cap.setCapability("app", "settings");
			cap.setCapability("noReset", "true");
			cap.setCapability("newCommandTimeout", "0");

			drv = new AppiumDriver(URL, cap);
			drv.resetApp();
			drv.manage().timeouts().implicitlyWait(2, TimeUnit.SECONDS);
			
			
			boolean zi = false;

			
			@SuppressWarnings("unchecked")
			List<MobileElement> el = (List<MobileElement>)drv.findElementsByAccessibilityId("Safari");
			
			
			while (!zi) {
			
			
				try {

					
					for  (int h = 0 ; h <el.size();h++) {
						

					
						MobileElement ell = el.get(h);	
						
						if (ell.isDisplayed()) {
							ell.click();
							zi = true;
							break;
						}
						
					
					}
					

					
					Map<String, Object> params = new HashMap<String, Object>();
				     
				    params.put("duration", "0.1");
				    params.put("direction", "down");
				    drv.executeScript("mobile:scroll", params);


				
				} catch (Exception e) {
						System.out.print(e);
					
				}
				
			}
			
			
			boolean zii = false;

			
			@SuppressWarnings("unchecked")
			List<MobileElement> elm = 
					(List<MobileElement>)drv.findElementsByAccessibilityId(
							"Clear History and Website Data");
			
			
			while (!zii) {
			
			
				try {


					for  (int h = 0 ; h <elm.size();h++) {
						

					
						MobileElement ell = elm.get(h);

						
						
						if (ell.isDisplayed()) {
							try {
							ell.click();
							zii = true;
							Thread.sleep(2000);
							drv.findElementByAccessibilityId("Clear History and Data").click();
							Thread.sleep(2000);
							return;}catch(Exception error) {return;}
						}
						
					
					}
					

					
					Map<String, Object> params = new HashMap<String, Object>();
				     
				    params.put("duration", "0.1");
				    params.put("direction", "down");
				    drv.executeScript("mobile:scroll", params);


				
				} catch (Exception e) {

					
				}
				
			}
							
		
		} else {
			
			drv.launchApp();
			
			boolean zii = false;

			
			@SuppressWarnings("unchecked")
			List<MobileElement> elm = 
					(List<MobileElement>)drv.findElementsByAccessibilityId(
							"Clear History and Website Data");
			
			
			while (!zii) {
			
			
				try {

					
					
					for  (int h = 0 ; h <elm.size();h++) {
						

						MobileElement ell = elm.get(h);
					
						
						if (ell.isDisplayed()) {
							try {
							ell.click();
							zii = true;
							Thread.sleep(2000);
							drv.findElementByAccessibilityId("Clear History and Data").click();
							Thread.sleep(2000);
							return;}catch(Exception error) {}
						}
						
					
					}
					

					
					Map<String, Object> params = new HashMap<String, Object>();
				     
				    params.put("duration", "0.1");
				    params.put("direction", "down");
				    drv.executeScript("mobile:scroll", params);


				
				} catch (Exception e) {

					
				}
				
			}
			
			
		}
		
	}
	
	
	public static Boolean ProcessWebPage(
			        @SuppressWarnings("rawtypes") 
			        AppiumDriver driver, 
					String Selector, 
					String direct) {
		
		
			int sc = 0;
			
			driver.manage().timeouts().implicitlyWait(15, TimeUnit.SECONDS);
			try {Thread.sleep(7000);}catch(Exception e) {}


			String js = "return document.evaluate(\"//span[contains(text(), '"+Selector+"')]\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;";
 
			
			WebElement elem = (WebElement)((JavascriptExecutor) driver).executeScript(js);

 
			driver.manage().timeouts().implicitlyWait(15, TimeUnit.SECONDS);
			
			try {
					String txt = elem.getText();
					//System.out.println(txt);
			} catch(Exception e) {
				
				return false;
			}

			WebElement parent = (WebElement) ((JavascriptExecutor) driver).executeScript(
					"return arguments[0].parentNode;", elem);
	 
			WebElement a = (WebElement) ((JavascriptExecutor) driver).executeScript(
					"return arguments[0].parentNode;", parent);
	 
			WebElement abs = (WebElement) ((JavascriptExecutor) driver).executeScript(
					"return arguments[0].parentNode;", a);
	 
			WebElement abd = (WebElement) ((JavascriptExecutor) driver).executeScript(
					"return arguments[0].parentNode;", abs);
			
			
			
			String js2 = "return document.evaluate(\"//span[contains(text(), '"+Selector+"')]\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;";
	 
			String Js = "";
	 
			String jsr = "var rect = arguments[0].getBoundingClientRect();var viewHeight = Math.max(document.documentElement.clientHeight, window.innerHeight); return !(rect.bottom < 0 || rect.top - viewHeight >= 0);";
	  
			
			Boolean z = false;		
			
			
			String JScript2 = "var elementRect = arguments[0].getBoundingClientRect(); var absoluteElementTop = elementRect.top + window.pageYOffset;const middle = absoluteElementTop - (window.innerHeight / 2);window.scrollTo(0, middle);";
			
			((JavascriptExecutor) driver).executeScript(
					JScript2, abd);
			
			z = (Boolean) ((JavascriptExecutor) driver).executeScript(
					jsr, abd);
			
	 
	 
			while (!z) {
				
				sc+=1;
				
				z = (Boolean) ((JavascriptExecutor) driver).executeScript(
						jsr, abd);
				System.out.println(abd.isDisplayed());
				if (abd.isDisplayed()) {break;}
				if (z) {break;}
		 
		 
				Map<String, Object> params = new HashMap<String, Object>();
				params.put("duration", "1");
				params.put("direction", direct);
				driver.executeScript("mobile:scroll", params);
				
				if (sc==8) {return false;}
	     
		 
			}
			

			WebElement Callbtn = null;
			int hg = 0;
			
			try {
			
				Callbtn = abd.findElement(By.cssSelector("a[role =\"button\"]"));

			}catch(Exception e) {
				
				Callbtn = abd.findElement(By.cssSelector("a"));
				hg =888;
			}
			
			z = (Boolean) ((JavascriptExecutor) driver).executeScript(
					jsr, Callbtn);
			
			driver.manage().timeouts().implicitlyWait(7, TimeUnit.SECONDS);
			
			if (z) {
	 

			try {
				try {

					Callbtn.click();

				}catch(Exception e) {
					System.out.print(e);
					
					Callbtn.click();
				}
				
			} catch (Exception e) {
				
				System.out.println(e);
			}
			} else {
				
				
				
				String JScript = "var elementRect = arguments[0].getBoundingClientRect(); var absoluteElementTop = elementRect.top + window.pageYOffset;const middle = absoluteElementTop - (window.innerHeight / 2);window.scrollTo(0, middle);";
				
				((JavascriptExecutor) driver).executeScript(
						JScript, Callbtn);
				
				z = (Boolean) ((JavascriptExecutor) driver).executeScript(
						jsr, Callbtn);
				
				if (z) {
					
				}else {
					
					Map<String, Object> params = new HashMap<String, Object>();
					params.put("duration", "0.5");
					params.put("direction", direct);
					driver.executeScript("mobile:scroll", params);
				}
				
				
			}
			driver.manage().timeouts().implicitlyWait(7, TimeUnit.SECONDS);

				 

				try {
					try {

						Callbtn.click();

					}catch(Exception e) {
						System.out.print(e);
						
						try {
						
						Callbtn.click();}catch(Exception err) {}
					}
				} catch (Exception e) {
					
					System.out.println(e);
				}
			
			
	 		driver.manage().timeouts().implicitlyWait(7, TimeUnit.SECONDS);
	 		try {Thread.sleep(2000);}catch(Exception errrr) {}
	 		
	 		boolean stop = false;
	 		
	 		if (hg==888) {return false;}
	 
	 		for (int cft  = 0;cft<3; cft++) {
	 			
	 			if (stop==true) {return true;}
		 
	 			try {
	 
	 				stop = DissmissAlert(Safari);
			 
	 			} catch(Exception e) {System.out.print(e);}
	 
	 		}	 
			
	 return true;


		
	}
	
}
