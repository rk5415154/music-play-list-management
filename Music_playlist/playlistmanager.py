import tkinter as tk
from tkinter import messagebox, filedialog
import random
import os

class Song:
    def __init__(self, title, artist, duration):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.next = None

class Playlist:
    def __init__(self):
        self.head = None

    def add_song(self, title, artist, duration, position=-1):
        new_song = Song(title, artist, duration)
        if position == 0 or not self.head:
            new_song.next = self.head
            self.head = new_song
        elif position == -1:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_song
        else:
            current = self.head
            index = 0
            while current.next and index < position - 1:
                current = current.next
                index += 1
            new_song.next = current.next
            current.next = new_song

    def remove_song(self, title):
        if not self.head:
            return False
        current = self.head
        prev = None
        while current and current.title != title:
            prev = current
            current = current.next
        if current:
            if prev:
                prev.next = current.next
            else:
                self.head = current.next
            return True
        return False

    def display_playlist(self):
        songs = []
        current = self.head
        while current:
            songs.append(f"{current.title} by {current.artist} ({current.duration}s)")
            current = current.next
        return "\n".join(songs)

    def move_song(self, from_pos, to_pos):
        if from_pos == to_pos or not self.head:
            return False

        prev_from, from_song = None, self.head
        pos = 0
        while from_song and pos < from_pos:
            prev_from = from_song
            from_song = from_song.next
            pos += 1
        if not from_song:
            return False
        if prev_from:
            prev_from.next = from_song.next
        else:
            self.head = from_song.next

        prev_to, to_song = None, self.head
        pos = 0
        while to_song and pos < to_pos:
            prev_to = to_song
            to_song = to_song.next
            pos += 1
        if to_pos == 0:
            from_song.next = self.head
            self.head = from_song
        else:
            prev_to.next = from_song
            from_song.next = to_song
        return True

    def search_song(self, title):
        current = self.head
        position = 0
        while current:
            if current.title == title:
                return position
            current = current.next
            position += 1
        return -1

    def save_playlist(self, filename):
        with open(filename, 'w') as file:
            current = self.head
            while current:
                file.write(f"{current.title},{current.artist},{current.duration}\n")
                current = current.next

    def load_playlist(self, filename):
        self.head = None
        with open(filename, 'r') as file:
            for line in file:
                title, artist, duration = line.strip().split(',')
                self.add_song(title, artist, int(duration))

    def shuffle_playlist(self):
        songs = []
        current = self.head
        while current:
            songs.append(current)
            current = current.next
        random.shuffle(songs)
        self.head = songs[0]
        for i in range(len(songs) - 1):
            songs[i].next = songs[i + 1]
        songs[-1].next = None

    def repeat_mode(self):
        if not self.head:
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = self.head

class PlaylistGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Playlist Manager develop by Raj Kumar")
        self.playlist = Playlist()

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Title:")
        self.title_label.grid(row=0, column=0)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1)

        self.artist_label = tk.Label(self.root, text="Artist:")
        self.artist_label.grid(row=1, column=0)
        self.artist_entry = tk.Entry(self.root)
        self.artist_entry.grid(row=1, column=1)

        self.duration_label = tk.Label(self.root, text="Duration (sec):")
        self.duration_label.grid(row=2, column=0)
        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.grid(row=2, column=1)

        self.add_button = tk.Button(self.root, text="Add Song", command=self.add_song)
        self.add_button.grid(row=3, column=0, columnspan=2)

        self.remove_button = tk.Button(self.root, text="Remove Song", command=self.remove_song)
        self.remove_button.grid(row=4, column=0, columnspan=2)

        self.display_button = tk.Button(self.root, text="Display Playlist", command=self.display_playlist)
        self.display_button.grid(row=5, column=0, columnspan=2)

        self.move_button = tk.Button(self.root, text="Move Song", command=self.move_song)
        self.move_button.grid(row=6, column=0, columnspan=2)

        self.search_button = tk.Button(self.root, text="Search Song", command=self.search_song)
        self.search_button.grid(row=7, column=0, columnspan=2)

        self.shuffle_button = tk.Button(self.root, text="Shuffle Playlist", command=self.shuffle_playlist)
        self.shuffle_button.grid(row=8, column=0, columnspan=2)

        self.save_button = tk.Button(self.root, text="Save Playlist", command=self.save_playlist)
        self.save_button.grid(row=9, column=0, columnspan=2)

        self.load_button = tk.Button(self.root, text="Load Playlist", command=self.load_playlist)
        self.load_button.grid(row=10, column=0, columnspan=2)

        self.output_text = tk.Text(self.root, height=10, width=60)
        self.output_text.grid(row=11, column=0, columnspan=2)

    def add_song(self):
        title = self.title_entry.get()
        artist = self.artist_entry.get()
        duration = int(self.duration_entry.get())
        self.playlist.add_song(title, artist, duration)
        messagebox.showinfo("Success", "Song added to playlist")

    def remove_song(self):
        title = self.title_entry.get()
        if self.playlist.remove_song(title):
            messagebox.showinfo("Success", "Song removed from playlist")
        else:
            messagebox.showwarning("Warning", "Song not found")

    def display_playlist(self):
        playlist_str = self.playlist.display_playlist()
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, playlist_str)

    def move_song(self):
        from_pos = int(self.title_entry.get())
        to_pos = int(self.artist_entry.get())
        if self.playlist.move_song(from_pos, to_pos):
            messagebox.showinfo("Success", "Song moved")
        else:
            messagebox.showwarning("Warning", "Invalid positions")

    def search_song(self):
        title = self.title_entry.get()
        position = self.playlist.search_song(title)
        if position != -1:
            messagebox.showinfo("Found", f"Song found at position {position}")
        else:
            messagebox.showwarning("Not Found", "Song not found")

    def shuffle_playlist(self):
        self.playlist.shuffle_playlist()
        messagebox.showinfo("Success", "Playlist shuffled")

    def save_playlist(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if filename:
            self.playlist.save_playlist(filename)
            messagebox.showinfo("Success", "Playlist saved")

    def load_playlist(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            self.playlist.load_playlist(filename)
            messagebox.showinfo("Success", "Playlist loaded")
            self.display_playlist()

if __name__ == "__main__":
    root = tk.Tk()
    app = PlaylistGUI(root)
    root.mainloop()
