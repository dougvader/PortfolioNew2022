using System;
using System.Collections;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;
using System.Web;
using Newtonsoft.Json.Linq;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Support.UI;
using Fastenshtein;
using System.Text;
using System.Globalization;
using System.Linq;

class Program
{
    static async Task Main()
    {
        try
        {
            var clientId = "AhAhAhhh";
            var clientSecret = "AhAhAhhh";
            var redirectUri = "http://localhost/"; // Replace with your redirect URI

            var authorizationCode = await GetAuthorizationCode(clientId, redirectUri);

            if (string.IsNullOrEmpty(authorizationCode))
            {
                System.Diagnostics.Debug.WriteLine("Failed to get authorization code.");
                return;
            }

            var accessToken = await GetAccessToken(clientId, clientSecret, redirectUri, authorizationCode);

            if (accessToken == null)
            {
                System.Diagnostics.Debug.WriteLine("Failed to get access token.");
                return;
            }

            string[] genres = 
            {                         
                "techno-peak-time-driving",
                "techno-raw-deep-hypnotic",
                "psy-trance",
                "trance-main-floor",
                "trance-raw-deep-hypnotic" 
            };

            foreach (var genre in genres)
            {
                var playlistId = await CreatePlaylist(accessToken, genre);
                if (playlistId != null)
                {
                    ArrayList tracks = await GetTracksForGenre(genre, accessToken);
                    tracks = await GetTrackUris(tracks, accessToken);
                    if (tracks.Count > 0)
                    {
                        await AddTracksToPlaylist(accessToken, playlistId, tracks);
                    }
                    else
                    {
                        System.Diagnostics.Debug.WriteLine($"No tracks found for genre: {genre}");
                    }
                }
                else
                {
                    System.Diagnostics.Debug.WriteLine($"Failed to create playlist for genre: {genre}");
                }
            }
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine("An error occurred: " + ex.Message);
        }
    }

    static async Task<string> GetAuthorizationCode(string clientId, string redirectUri)
    {
        using (var driver = new ChromeDriver())
        {
            driver.Navigate().GoToUrl($"https://accounts.spotify.com/authorize" +
                $"?client_id={clientId}" +
                $"&response_type=code" +
                $"&redirect_uri={redirectUri}" +
                $"&scope=playlist-modify-public");

            WebDriverWait wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));
            IWebElement fbButton_wait = wait.Until(SeleniumExtras.WaitHelpers.ExpectedConditions.ElementIsVisible(By.ClassName("Button-sc-y0gtbx-0")));
            var buttons = driver.FindElements(By.ClassName("Button-sc-y0gtbx-0"));
            if (buttons.Count > 0)
            {
                buttons[1].Click();
            }

            wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));
            IWebElement emailInput = wait.Until(SeleniumExtras.WaitHelpers.ExpectedConditions.ElementIsVisible(By.Id("email")));
            emailInput.SendKeys("");
            IWebElement passwordInput = driver.FindElement(By.Id("pass"));
            passwordInput.SendKeys("");

            IWebElement loginButton = driver.FindElement(By.Id("loginbutton"));
            loginButton.Click();

            wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));
            var currentUrl = driver.Url;
            System.Diagnostics.Debug.WriteLine(currentUrl);
            while (currentUrl.Length <= redirectUri.Length)
            {
                await Task.Delay(1000);
                currentUrl = driver.Url;
            }

            var uri = new Uri(currentUrl);
            var authorizationCode = uri.Query.Substring(uri.Query.IndexOf("code=") + 5);
            return authorizationCode;
        }
    }

    static async Task<string> GetAccessToken(string clientId, string clientSecret, string redirectUri, string code)
    {
        try
        {
            using (var client = new HttpClient())
            {
                var formData = new FormUrlEncodedContent(new[]
                {
                    new KeyValuePair<string, string>("grant_type", "authorization_code"),
                    new KeyValuePair<string, string>("code", code),
                    new KeyValuePair<string, string>("redirect_uri", redirectUri),
                    new KeyValuePair<string, string>("client_id", clientId),
                    new KeyValuePair<string, string>("client_secret", clientSecret)
                });

                var response = await client.PostAsync("https://accounts.spotify.com/api/token", formData);
                var responseContent = await response.Content.ReadAsStringAsync();
                System.Diagnostics.Debug.WriteLine(responseContent);

                dynamic json = JObject.Parse(responseContent);
                return json.access_token;
            }
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine("Error getting access token: " + ex.Message);
            return null;
        }
    }

    static async Task<string> CreatePlaylist(string accessToken, string genre)
    {
        var genre_iterator = 0;

        string[] genres_list_fancy = new string[]
        {
            "Techno (Peak-Time/Driving)",
            "Techno (Raw / Deep / Hypnotic)", 
            "Psy-Trance", 
            "Trance (Main Floor)", 
            "Trance (Raw / Deep / Hypnotic)"
        };

        string[] genres_list = new string[]
        {
            "techno-peak-time-driving",
            "techno-raw-deep-hypnotic",
            "psy-trance",
            "trance-main-floor",
            "trance-raw-deep-hypnotic"
        };
        try
        {
            for (int i = 0; i <= genres_list.Length - 1; i++)
            {
                if (genres_list[i] == genre)
                {
                    genre_iterator = i;
                }
            }

            var name = genres_list_fancy[genre_iterator] + " Beatport Top 100_" + CultureInfo.CurrentCulture.DateTimeFormat.GetMonthName((DateTime.Today.Month)) + "_" + DateTime.Today.Year;
            var description = "The best " + genre + " " + DateTime.Today.Month + "_" + DateTime.Today.Year;

            using (var client = new HttpClient())
            {
                client.DefaultRequestHeaders.Add("Authorization", "Bearer " + accessToken);
                var content = new StringContent(
                    "{\"name\":\"" + name + "\",\"description\":\"" + description + "\",\"public\":true}",
                    System.Text.Encoding.UTF8,
                    "application/json"
                );

                var response = await client.PostAsync("https://api.spotify.com/v1/me/playlists", content);
                var responseContent = await response.Content.ReadAsStringAsync();
                System.Diagnostics.Debug.WriteLine(responseContent);

                dynamic json = JObject.Parse(responseContent);
                return json.id;
            }
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine("Error creating playlist: " + ex.Message);
            return null;
        }
    }

    static async Task<ArrayList> GetTracksForGenre(string genre, string accessToken)
    {
        string[] genres_list = new string[]
        {
            "techno-peak-time-driving/6",
            "techno-raw-deep-hypnotic/92",
            "psy-trance/13",
            "trance-main-floor/7",
            "trance-raw-deep-hypnotic/99"
        };

        string link = "";

        for (int i=0; i < genres_list.Length; i++)
        {
            if (genres_list[i].Contains(genre)) {
                link = genres_list[i];
            }
        }
        

        ArrayList tracks = new ArrayList();

        try
        {
            using (var driver = new ChromeDriver())
            {
                driver.Navigate().GoToUrl($"https://www.beatport.com/genre/" + link + "/top-100");

                await Task.Delay(7000);

                for (int i = 1; i <= 100; i++)
                {
                    string script = $"return document.querySelectorAll('[class^=\"TracksList-style\"]').item(0).children.item({i}).children.item(1).innerText";
                    string trackInfo = (string)((IJavaScriptExecutor)driver).ExecuteScript(script);

                    string[] parts = trackInfo.Split('\n');
                    if (parts.Length >= 3)
                    {
                        string trackName = parts[1].Trim();
                        string artistName = parts[2];
                        System.Diagnostics.Debug.WriteLine("track name is " + trackName);
                        System.Diagnostics.Debug.WriteLine("artist name is " + artistName);

                        tracks.Add(artistName + "/" + trackName);
                    }
                }
            }
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine("Error occurred: " + ex.Message);
        }

        return tracks;
    }

    static async Task<ArrayList> GetTrackUris(ArrayList tracks, string accessToken)
    {
        ArrayList uris = new ArrayList();

        try
        {
            foreach (string track in tracks)
            {
                string[] parts = track.Split('/');
                var artistName = parts[0].Trim();
                var trackName = parts[1].Trim();

                // Remove mix type suffixes from trackName
                trackName = RemoveMixType(trackName);

                // Construct the Spotify search URL
                string searchUrl = $"https://api.spotify.com/v1/search?q=track:{HttpUtility.UrlEncode(trackName)}%20artist:{HttpUtility.UrlEncode(artistName)}&type=track";

                using (var client = new HttpClient())
                {
                    // Add authorization header with the access token
                    client.DefaultRequestHeaders.Add("Authorization", "Bearer " + accessToken);

                    // Send GET request to Spotify search URL
                    var response = await client.GetAsync(searchUrl);
                    response.EnsureSuccessStatusCode();

                    // Extract the JSON response
                    string jsonResponse = await response.Content.ReadAsStringAsync();
                    System.Diagnostics.Debug.WriteLine("JSON response is " + jsonResponse.ToString());

                    // Parse the JSON response
                    JObject searchResults = JObject.Parse(jsonResponse);

                    // Extract the tracks from the search results
                    JToken[] jtracks = searchResults["tracks"]["items"].ToArray();
                    System.Diagnostics.Debug.WriteLine($"Found {jtracks.Length} tracks in search results");

                    // Keep track of whether a URI for this track has been found
                    bool uriFound = false;

                    // Loop through each track found
                    foreach (JToken jt in jtracks)
                    {
                        // Extract the track name from the response
                        string foundTrackName = (string)jt["name"];

                        // Extract the artists from the response
                        var artists = ((JArray)jt["artists"]).Select(a => (string)a["name"]).ToList();

                        // Check if any track name matches the input track name(s) and no URI has been found yet
                        if (Fastenshtein.Levenshtein.Distance(foundTrackName, trackName) <= 15 && !uriFound)
                        {
                            // Check if any artist name matches the input artist name(s)
                            if (artists.Any(a => Fastenshtein.Levenshtein.Distance(a, artistName) <= 15))
                            {
                                // If both track name and artist name(s) match, return the track URI
                                string trackUri = (string)jt["uri"];
                                uris.Add(trackUri);
                                System.Diagnostics.Debug.WriteLine("Track URI found!");
                                // Mark that a URI for this track has been found
                                uriFound = true;
                            }
                            else
                            {
                                System.Diagnostics.Debug.WriteLine("It was not a match");
                            }
                        }
                    }
                }
            }
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine("Error occurred: " + ex.Message);
        }

        return uris;
    }

    static async Task AddTracksToPlaylist(string accessToken, string playlistId, ArrayList tracks)
    {
        try
        {
            // Spotify API has a limit on the number of track URIs per request
            const int batchSize = 100;

            // Divide tracks into batches
            for (int i = 0; i < tracks.Count; i += batchSize)
            {
                // Get a batch of track URIs
                var batch = tracks.GetRange(i, Math.Min(batchSize, tracks.Count - i));

                // Construct a list of track URIs
                List<string> trackUris = new List<string>();
                foreach (var track in batch)
                {
                    // Assuming the track object contains the URI in the third position
                    trackUris.Add((string)track);
                }

                // Create a JSON payload containing the track URIs
                string jsonPayload = Newtonsoft.Json.JsonConvert.SerializeObject(new
                {
                    uris = trackUris
                });

                // Construct the URL
                string url = $"https://api.spotify.com/v1/playlists/{playlistId}/tracks";

                using (var client = new HttpClient())
                {
                    // Add authorization header with the access token
                    client.DefaultRequestHeaders.Add("Authorization", "Bearer " + accessToken);

                    // Create StringContent with JSON payload
                    var content = new StringContent(jsonPayload, Encoding.UTF8, "application/json");

                    // Send POST request to Spotify API endpoint
                    var response = await client.PostAsync(url, content);

                    // Log response content for debugging
                    string responseContent = await response.Content.ReadAsStringAsync();
                    System.Diagnostics.Debug.WriteLine("Response content: " + responseContent);

                    // Check if request was successful
                    if (response.IsSuccessStatusCode)
                    {
                        System.Diagnostics.Debug.WriteLine("Tracks added to the playlist successfully.");
                    }
                    else
                    {
                        System.Diagnostics.Debug.WriteLine("Failed to add tracks to the playlist. Status code: " + response.StatusCode);
                    }
                }
            }
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine("Error occurred: " + ex.Message);
        }
    }

    static string RemoveMixType(string trackName)
    {
        // Define common mix type suffixes
        string[] mixTypes = { "original mix", "extended mix", "club mix", "remix", "dub", "edit", "radio edit" };

        // Iterate over mix types and remove them from trackName
        foreach (var mixType in mixTypes)
        {
            if (trackName.EndsWith(mixType, StringComparison.OrdinalIgnoreCase))
            {
                // Remove mix type and trim any trailing whitespace
                trackName = trackName.Substring(0, trackName.Length - mixType.Length).TrimEnd();
                break; // Stop after removing the first mix type found
            }
        }

        return trackName;
    }
}
