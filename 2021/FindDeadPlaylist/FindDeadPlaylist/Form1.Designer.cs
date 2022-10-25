
namespace FindDeadPlaylist
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.select_playlist_label = new System.Windows.Forms.Label();
            this.playlist_textbox = new System.Windows.Forms.RichTextBox();
            this.select_playlist_button = new System.Windows.Forms.Button();
            this.output_location_button = new System.Windows.Forms.Button();
            this.output_textbox = new System.Windows.Forms.RichTextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.search_location_button = new System.Windows.Forms.Button();
            this.search_textbox = new System.Windows.Forms.RichTextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.go_button = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // select_playlist_label
            // 
            this.select_playlist_label.AutoSize = true;
            this.select_playlist_label.Location = new System.Drawing.Point(55, 19);
            this.select_playlist_label.Name = "select_playlist_label";
            this.select_playlist_label.Size = new System.Drawing.Size(65, 15);
            this.select_playlist_label.TabIndex = 0;
            this.select_playlist_label.Text = "Playlist File";
            // 
            // playlist_textbox
            // 
            this.playlist_textbox.Location = new System.Drawing.Point(126, 15);
            this.playlist_textbox.Name = "playlist_textbox";
            this.playlist_textbox.Size = new System.Drawing.Size(239, 24);
            this.playlist_textbox.TabIndex = 1;
            this.playlist_textbox.Text = "select playlyist file ->";
            // 
            // select_playlist_button
            // 
            this.select_playlist_button.Location = new System.Drawing.Point(371, 15);
            this.select_playlist_button.Name = "select_playlist_button";
            this.select_playlist_button.Size = new System.Drawing.Size(26, 23);
            this.select_playlist_button.TabIndex = 2;
            this.select_playlist_button.Text = "...";
            this.select_playlist_button.UseVisualStyleBackColor = true;
            this.select_playlist_button.Click += new System.EventHandler(this.select_playlist_button_Click);
            // 
            // output_location_button
            // 
            this.output_location_button.Location = new System.Drawing.Point(371, 54);
            this.output_location_button.Name = "output_location_button";
            this.output_location_button.Size = new System.Drawing.Size(26, 23);
            this.output_location_button.TabIndex = 5;
            this.output_location_button.Text = "...";
            this.output_location_button.UseVisualStyleBackColor = true;
            this.output_location_button.Click += new System.EventHandler(this.output_location_button_Click);
            // 
            // output_textbox
            // 
            this.output_textbox.Location = new System.Drawing.Point(126, 54);
            this.output_textbox.Name = "output_textbox";
            this.output_textbox.Size = new System.Drawing.Size(239, 24);
            this.output_textbox.TabIndex = 4;
            this.output_textbox.Text = "choose output location ->";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 57);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(108, 15);
            this.label1.TabIndex = 3;
            this.label1.Text = "Output Destination";
            // 
            // search_location_button
            // 
            this.search_location_button.Location = new System.Drawing.Point(371, 94);
            this.search_location_button.Name = "search_location_button";
            this.search_location_button.Size = new System.Drawing.Size(26, 23);
            this.search_location_button.TabIndex = 8;
            this.search_location_button.Text = "...";
            this.search_location_button.UseVisualStyleBackColor = true;
            this.search_location_button.Click += new System.EventHandler(this.search_location_button_Click);
            // 
            // search_textbox
            // 
            this.search_textbox.Location = new System.Drawing.Point(126, 94);
            this.search_textbox.Name = "search_textbox";
            this.search_textbox.Size = new System.Drawing.Size(239, 24);
            this.search_textbox.TabIndex = 7;
            this.search_textbox.Text = "choose search directory ->";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 97);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(91, 15);
            this.label2.TabIndex = 6;
            this.label2.Text = "Search Location";
            // 
            // go_button
            // 
            this.go_button.Location = new System.Drawing.Point(126, 142);
            this.go_button.Name = "go_button";
            this.go_button.Size = new System.Drawing.Size(239, 23);
            this.go_button.TabIndex = 9;
            this.go_button.Text = "Go!";
            this.go_button.UseVisualStyleBackColor = true;
            this.go_button.Click += new System.EventHandler(this.go_button_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(410, 193);
            this.Controls.Add(this.go_button);
            this.Controls.Add(this.search_location_button);
            this.Controls.Add(this.search_textbox);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.output_location_button);
            this.Controls.Add(this.output_textbox);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.select_playlist_button);
            this.Controls.Add(this.playlist_textbox);
            this.Controls.Add(this.select_playlist_label);
            this.Name = "Form1";
            this.Text = "Find Dead Playlist";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label select_playlist_label;
        private System.Windows.Forms.RichTextBox playlist_textbox;
        private System.Windows.Forms.Button select_playlist_button;
        private System.Windows.Forms.Button output_location_button;
        private System.Windows.Forms.RichTextBox output_textbox;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button search_location_button;
        private System.Windows.Forms.RichTextBox search_textbox;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Button go_button;
    }
}

