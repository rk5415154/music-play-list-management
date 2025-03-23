#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <algorithm>
#include <cstdlib>
#include <ctime>

using namespace std;

class Song {
public:
    string title;
    string artist;
    int duration;  // in seconds
    Song* next;

    Song(string t, string a, int d) : title(t), artist(a), duration(d), next(nullptr) {}

    void display() const {
        cout << title << " by " << artist << ", Duration: " << duration << " seconds" << endl;
    }
};

class Playlist {
private:
    Song* head;

public:
    Playlist() : head(nullptr) {}

    // 1. Add Song
    void addSong(const string& title, const string& artist, int duration, int position = -1) {
        Song* newSong = new Song(title, artist, duration);
        if (position == 0 || head == nullptr) {  // Add at the beginning
            newSong->next = head;
            head = newSong;
        } else if (position == -1) {  // Add at the end
            Song* current = head;
            while (current->next) {
                current = current->next;
            }
            current->next = newSong;
        } else {  // Add at a specific position
            Song* current = head;
            int index = 0;
            while (current->next && index < position - 1) {
                current = current->next;
                ++index;
            }
            newSong->next = current->next;
            current->next = newSong;
        }
    }

    // 2. Remove Song
    void removeSong(const string& title) {
        if (!head) {
            cout << "Playlist is empty" << endl;
            return;
        }
        Song* current = head;
        Song* prev = nullptr;
        while (current && current->title != title) {
            prev = current;
            current = current->next;
        }
        if (current) {
            if (prev) {
                prev->next = current->next;
            } else {
                head = current->next;
            }
            delete current;
            cout << "Song removed successfully" << endl;
        } else {
            cout << "Song not found" << endl;
        }
    }

    // 3. Display Playlist
    void displayPlaylist() const {
        Song* current = head;
        int position = 1;
        int totalDuration = 0;
        while (current) {
            cout << position << ": ";
            current->display();
            totalDuration += current->duration;
            current = current->next;
            ++position;
        }
        cout << "Total duration: " << totalDuration << " seconds" << endl;
    }

    // 4. Move Song
    void moveSong(int fromPos, int toPos) {
        if (fromPos == toPos || !head) return;

        // Remove song at `fromPos`
        Song* current = head;
        Song* prev = nullptr;
        int pos = 0;
        while (current && pos < fromPos) {
            prev = current;
            current = current->next;
            ++pos;
        }
        if (!current) {
            cout << "Invalid position" << endl;
            return;
        }
        Song* songToMove = current;
        if (prev) prev->next = current->next;
        else head = current->next;

        // Insert at `toPos`
        if (toPos == 0) {
            songToMove->next = head;
            head = songToMove;
        } else {
            current = head;
            prev = nullptr;
            pos = 0;
            while (current && pos < toPos) {
                prev = current;
                current = current->next;
                ++pos;
            }
            prev->next = songToMove;
            songToMove->next = current;
        }
    }

    // 5. Search for a Song
    void searchSong(const string& title) const {
        Song* current = head;
        int position = 1;
        while (current) {
            if (current->title == title) {
                cout << "Found '" << title << "' by " << current->artist << " at position " << position << endl;
                return;
            }
            current = current->next;
            ++position;
        }
        cout << "Song not found" << endl;
    }

    // 6. Save & Load Playlist
    void savePlaylist(const string& filename) const {
        ofstream file(filename);
        Song* current = head;
        while (current) {
            file << current->title << "," << current->artist << "," << current->duration << endl;
            current = current->next;
        }
        file.close();
    }

    void loadPlaylist(const string& filename) {
        ifstream file(filename);
        string line;
        head = nullptr;
        while (getline(file, line)) {
            size_t pos1 = line.find(',');
            size_t pos2 = line.find(',', pos1 + 1);
            string title = line.substr(0, pos1);
            string artist = line.substr(pos1 + 1, pos2 - pos1 - 1);
            int duration = stoi(line.substr(pos2 + 1));
            addSong(title, artist, duration, -1);
        }
        file.close();
    }

    // Shuffle Playlist
    void shufflePlaylist() {
        vector<Song*> songs;
        Song* current = head;
        while (current) {
            songs.push_back(current);
            current = current->next;
        }
        random_shuffle(songs.begin(), songs.end());
        head = songs[0];
        for (size_t i = 0; i < songs.size() - 1; ++i) {
            songs[i]->next = songs[i + 1];
        }
        songs.back()->next = nullptr;
    }

    // Repeat Mode
    void repeatMode() {
        if (!head) return;
        Song* current = head;
        while (current->next) {
            current = current->next;
        }
        current->next = head;  // Last song points back to the first song
    }
};

int main() {
    Playlist playlist;
    int option;
    string title, artist;
    int duration, position;

    while (true) {
        cout << "\nOptions:\n1. Add Song\n2. Remove Song\n3. Display Playlist\n4. Move Song\n5. Search for a Song\n";
        cout << "6. Save Playlist\n7. Load Playlist\n8. Shuffle Playlist\n9. Repeat Mode\n10. Exit\nChoose an option: ";
        cin >> option;

        switch (option) {
            case 1:
                cout << "Enter title: ";
                cin.ignore();
                getline(cin, title);
                cout << "Enter artist: ";
                getline(cin, artist);
                cout << "Enter duration (in seconds): ";
                cin >> duration;
                cout << "Enter position (or -1 to add to end): ";
                cin >> position;
                playlist.addSong(title, artist, duration, position);
                break;

            case 2:
                cout << "Enter title to remove: ";
                cin.ignore();
                getline(cin, title);
                playlist.removeSong(title);
                break;

            case 3:
                playlist.displayPlaylist();
                break;

            case 4:
                int fromPos, toPos;
                cout << "Enter current position: ";
                cin >> fromPos;
                cout << "Enter new position: ";
                cin >> toPos;
                playlist.moveSong(fromPos, toPos);
                break;

            case 5:
                cout << "Enter title to search for: ";
                cin.ignore();
                getline(cin, title);
                playlist.searchSong(title);
                break;

            case 6:
                playlist.savePlaylist("playlist.txt");
                break;

            case 7:
                playlist.loadPlaylist("playlist.txt");
                break;

            case 8:
                playlist.shufflePlaylist();
                cout << "Playlist shuffled" << endl;
                break;

            case 9:
                playlist.repeatMode();
                cout << "Repeat mode enabled" << endl;
                break;

            case 10:
                return 0;

            default:
                cout << "Invalid option" << endl;
        }
    }
    return 0;
}
