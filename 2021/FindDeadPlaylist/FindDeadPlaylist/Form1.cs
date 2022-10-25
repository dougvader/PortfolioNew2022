using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Diagnostics;
using System.IO;
using System.Security;
using System.Security.Permissions;

namespace FindDeadPlaylist
{
    public partial class Form1 : Form
    {
        private string playlist_location;
        private string output_location;
        private string search_location;
        private List<string> filenames;
        private const string search_pattern = "*.mp3";
        private const SearchOption search_option = SearchOption.AllDirectories;
        private EnumerationOptions e_options = new EnumerationOptions()
        {
            IgnoreInaccessible = true,
            AttributesToSkip = FileAttributes.Hidden | FileAttributes.System,
            RecurseSubdirectories = true
        };


        public Form1()
        {
            InitializeComponent();
        }

        private void select_playlist_button_Click(object sender, EventArgs e)
        {
            using (OpenFileDialog open_playlist_explorer_window = new OpenFileDialog())
            {
                open_playlist_explorer_window.Title = "Choose .m3u file";
                open_playlist_explorer_window.InitialDirectory = @"c:\\";
                open_playlist_explorer_window.DefaultExt = "m3u";
                open_playlist_explorer_window.Filter = "m3u files (*.m3u)|*.m3u|All files (*.*)|*.*";
                open_playlist_explorer_window.FilterIndex = 2;
                open_playlist_explorer_window.RestoreDirectory = true;

                if (open_playlist_explorer_window.ShowDialog() == DialogResult.OK)
                {
                    playlist_location = open_playlist_explorer_window.FileName;
                    playlist_textbox.Text = playlist_location;
                }
            }
        }

        private void output_location_button_Click(object sender, EventArgs e)
        {
            using (FolderBrowserDialog output_destination_explorer_window = new FolderBrowserDialog())
            {
                output_destination_explorer_window.Description = "Choose output folder";
                DialogResult result = output_destination_explorer_window.ShowDialog();

                if (result == DialogResult.OK && !string.IsNullOrWhiteSpace(output_destination_explorer_window.SelectedPath))
                {
                    output_location = output_destination_explorer_window.SelectedPath;
                    output_textbox.Text = output_location;
                }
            }
        }

        private void search_location_button_Click(object sender, EventArgs e)
        {
            using (FolderBrowserDialog search_location_explorer_window = new FolderBrowserDialog())
            {
                search_location_explorer_window.Description = "Choose output folder";
                DialogResult result = search_location_explorer_window.ShowDialog();

                if (result == DialogResult.OK && !string.IsNullOrWhiteSpace(search_location_explorer_window.SelectedPath))
                {
                    search_location = search_location_explorer_window.SelectedPath;
                    search_textbox.Text = search_location;
                }
            }
        }

        private void go_button_Click(object sender, EventArgs e)
        {
            if (search_textbox.Text != null && playlist_textbox.Text != null && output_textbox.Text != null)
            {
                var new_directory = System.IO.Directory.CreateDirectory(output_location);
                //open playlist file and get file names
                var playlist = System.IO.File.ReadAllLines(playlist_location);
                filenames = new List<string>(playlist.Length);
                foreach (string file in playlist)  
                {
                    filenames.Add(file);
                }

                //for each track in playlist
                //foreach (string playlist_file in filenames)
                //{
                try
                {
                    // conduct search to find file that matches missing file name
                    Debug.WriteLine("Conducting search...");                      
                    var files_found = SafeWalk.EnumerateFiles(search_location, search_pattern, search_option, filenames);
                    var unable_to_find_list = filenames;

                    // for each file found, copy that file to the output folder
                    foreach (var file in files_found)
                    {
                        Debug.WriteLine("adding track to folder " + file);
                        unable_to_find_list.Remove(file);
                        System.IO.File.Copy(file, Path.Combine(output_location, Path.GetFileName(file)), true);
                    }
                    // create a new playlist file for each file that wasn't found
                    var unable_to_find_text = System.IO.File.CreateText(Name = "unable_to_find");


                    // for each file it could not find, add it to "unable_to_find" text file
                    foreach (var file in unable_to_find_list)
                    {
                        unable_to_find_text.WriteLine(file);
                    }
                    unable_to_find_text.Close();

                    Debug.WriteLine(files_found.Count() + " dead songs found and added to output foler.");
                    Debug.WriteLine(unable_to_find_list.Count() + " dead songs not found.");


                } catch(Exception ex)
                {
                    //continue;
                }                       
                //}
            } else { 
                // Show popup "Please enter terms for each field"
            }
        }
       
        public static int Compute(string s, string t)
        {
            if (string.IsNullOrEmpty(s))
            {
                if (string.IsNullOrEmpty(t))
                    return 0;
                return t.Length;
            }

            if (string.IsNullOrEmpty(t))
            {
                return s.Length;
            }

            int n = s.Length;
            int m = t.Length;
            int[,] d = new int[n + 1, m + 1];

            // initialize the top and right of the table to 0, 1, 2, ...
            for (int i = 0; i <= n; d[i, 0] = i++) ;
            for (int j = 1; j <= m; d[0, j] = j++) ;

            for (int i = 1; i <= n; i++)
            {
                for (int j = 1; j <= m; j++)
                {
                    int cost = (t[j - 1] == s[i - 1]) ? 0 : 1;
                    int min1 = d[i - 1, j] + 1;
                    int min2 = d[i, j - 1] + 1;
                    int min3 = d[i - 1, j - 1] + cost;
                    d[i, j] = Math.Min(Math.Min(min1, min2), min3);
                }
            }
            return d[n, m];
        }
    }
    public static class SafeWalk
    {
        public static IEnumerable<string> EnumerateFiles(string path, string searchPattern, SearchOption searchOpt, List<string> dead_tracks)
        {
            List<string> files = new List<string>() { };

            try
            {
                Parallel.ForEach(Directory.EnumerateFiles(path, searchPattern, searchOpt), file =>
                {
                    Parallel.For(0, dead_tracks.Count, index =>
                    {
                        if (dead_tracks[index].Equals(Path.GetFileName(file)))
                        {
                            files.Add(file);
                        }
                        else
                        {
                            return;
                        }
                    });
                });
            } catch (Exception ex)
            {
                return Enumerable.Empty<string>();
            }

            return files;

            /*            if (searchOpt == SearchOption.TopDirectoryOnly)
                        {
                            List<string> T = new List<string>() { };
                            Parallel.ForEach(Directory.EnumerateFiles(path, searchPattern, SearchOption.TopDirectoryOnly), file_found =>
                                Parallel.For(0, dead_tracks.Count, index =>
                                {
                                    if (dead_tracks[index].Equals(Path.GetFileName(file_found)))
                                    {
                                        T.Add(file_found);
                                    }
                                }));
                            return T;
                        }*/

            /*List<string> folders = new List<string>() { path };
            int folCount = 1;
            List<string> files = new List<string>() { };

            try
            {   //for each folder...
                Parallel.For(0, folCount, index =>
                {                                       
                    try
                    {
                        //for each sub folder...
                        Parallel.ForEach(Directory.EnumerateDirectories(folders[index], "*", SearchOption.TopDirectoryOnly), newDir =>
                        {
                            try
                            {
                                folders.Add(newDir);
                                Debug.Print("will search directory " + newDir);
                                folCount++;
                                Debug.Print("folder count is " + folCount);

                                //for each file in each folder
                                Parallel.ForEach(Directory.EnumerateFiles(newDir, searchPattern), file =>
                                {                                   
                                    try
                                    {   
                                        //for each dead track
                                        Parallel.For(0, dead_tracks.Count, index2 =>
                                        {
                                            //Debug.Print("searching directory " + newDir + " for track " + dead_tracks[index2]);
                                            if (dead_tracks[index2].Equals(Path.GetFileName(file)))
                                            {
                                                Debug.Print("track matched");
                                                files.Add(file);
                                            }
                                            else
                                            {
                                                //continue;
                                                //Debug.Print("track did not match");
                                                return;
                                            }
                                        });
                                        return;
                                    } catch (Exception ex)
                                    {
                                        Debug.Print("Ex when matching tracks");
                                        return;
                                    }
                                });
                            }
                            catch (Exception ex)
                            {
                                Debug.Print("Ex when searching files");
                                return;
                            }
                            return;
                        });
                    }
                    catch (Exception ex)
                    {
                        Debug.Print("this was the last exception before it broke " + ex);
                        return;
                    }
                    return;
                });
            }
            catch (Exception ex)
            {
                Debug.Print("Ex when searching folders");
                return Enumerable.Empty<string>();
            }*/

            //return files;
        }
    }
}
