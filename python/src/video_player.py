"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
from .command_parser import CommandException
import operator
import random, copy


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._currentVideo = None
        self._paused = False
        self._allPlaylists = {}
        self._currentPlaylist = None
        self._undo = False
        self._lastCommand = None

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

        if self._undo:
                self._undo = False

    def show_all_videos(self):
        """Returns all videos."""
        all_videos = self._video_library.get_all_videos()
        print("Here's a list of all available videos:")
        for video in sorted(all_videos, key=operator.attrgetter('_title')):
            tags = " ".join(video._tags)
            if video._flag is False:
                print(f"  {video._title} ({video._video_id}) [{tags}]")
            else:
                print(f"  {video._title} ({video._video_id}) [{tags}] - FLAGGED (reason: {video._flagreason})")
        if self._undo:
                self._undo = False
            
    def play_video(self, video_id):
        """Plays the respective video.
        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        if video == None:
            print("Cannot play video: Video does not exist")
        else:
            if video._flag is True:
                print(f"Cannot play video: Video is currently flagged (reason: {video._flagreason})")
            else:
                if self._currentVideo is not None:
                    print("Stopping video:", self._currentVideo._title)

                print("Playing video:", video._title)
                self._currentVideo, self._paused = video, False
                if not self._undo:
                    """For undo command"""
                    self._lastCommand = 1 
                else:
                    self._undo = False

    def stop_video(self):
        """Stops the current video."""
        if self._currentVideo is not None:
            print("Stopping video:", self._currentVideo._title)
            self._previousVideo, self._previousPlaylist = self._currentVideo, self._currentPlaylist # For undo command
            self._currentVideo, self._paused, self._currentPlaylist = None, False, None
            if not self._undo:
                """For undo command"""
                self._lastCommand = 2 
            else:
                self._undo = False
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        all_videos = self._video_library.get_all_videos()
        filtered_videos = list(filter(lambda video: video._flag is False, all_videos))
        num_videos = len(filtered_videos)
        if num_videos is 0:
            print("No videos available")
        else:
            self.play_video(filtered_videos[random.choice(range(num_videos))]._video_id)

            if not self._undo:
                """For undo command"""
                self._lastCommand = 3 
            else:
                self._undo = False

    def pause_video(self):
        """Pauses the current video."""
        if self._currentVideo is None:
            print("Cannot pause video: No video is currently playing")
        else:
            if not self._paused:
                print("Pausing video:", self._currentVideo._title)
                self._paused = True
                if not self._undo:
                    """For undo command"""
                    self._lastCommand = 4 
                else:
                    self._undo = False
            else:
                print("Video already paused:", self._currentVideo._title)
        
    def continue_video(self):
        """Resumes playing the current video."""
        if self._currentVideo is None:
            print("Cannot continue video: No video is currently playing")
        else:
            if self._paused:
                print("Continuing video:", self._currentVideo._title)
                self._paused = False
                if not self._undo:
                    """For undo command"""
                    self._lastCommand = 5 
                else:
                    self._undo = False
            else:
                print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""
        if self._currentVideo is None:
            print("No video is currently playing")
        else:
            tags = " ".join(self._currentVideo._tags) 
            video_info = f"{self._currentVideo._title} ({self._currentVideo._video_id}) [{tags}]"
            if not self._paused:
                print("Currently playing:", video_info)
            else:
                print("Currently playing:", video_info, "- PAUSED")
        if self._undo:
                self._undo = False

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in self._allPlaylists.keys():
            print("Successfully created new playlist:", playlist_name)
            self._allPlaylists[playlist_name.lower()] = Playlist(playlist_name)
            if not self._undo:
                """For undo command"""
                self._lastCommand = 6 
            else:
                self._undo = False
        else:
            print("Cannot create playlist: A playlist with the same name already exists")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        if playlist_name.lower() not in self._allPlaylists.keys():
            """ Check if playlist exists"""
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
        else:
            video = self._video_library.get_video(video_id)
            if video is None:
                """ Check if video exists in the library"""
                print(f"Cannot add video to {playlist_name}: Video does not exist")
            else:
                if video._flag is True:
                    print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {video._flagreason})")
                else: 
                    playlist = self._allPlaylists[playlist_name.lower()]
                    playlist.add_video(playlist_name, video)
                    self._latest_video_added_to_playlist = [playlist_name, video_id] # For undo Command
                    if not self._undo:
                        """For undo command"""
                        self._lastCommand = 7 
                    else:
                        self._undo = False
            
    def show_all_playlists(self):
        """Display all playlists."""
        if not self._allPlaylists:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            for playlist in sorted(self._allPlaylists):
                print(f"  {self._allPlaylists[playlist]._playlist_name}")

        if self._undo:
                self._undo = False

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self._allPlaylists.get(playlist_name.lower(), None)
        if playlist is None:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
        else:
            playlist.show_videos(playlist_name)

        if self._undo:
                self._undo = False

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist = self._allPlaylists.get(playlist_name.lower(), None)
        if playlist is None:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
        else:
            video = self._video_library.get_video(video_id)
            if video is None: 
                print(f"Cannot remove video from {playlist_name}: Video does not exist")
            else:
                playlist.remove_video(playlist_name, video_id)
                self._latest_video_removed_from_playlist = [playlist_name, video_id] # For undo command
                if not self._undo:
                    """For undo command"""
                    self._lastCommand = 8 
                else:
                    self._undo = False

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self._allPlaylists.get(playlist_name.lower(), None)
        if playlist is None:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
        else:
            self._latest_clearedPlaylist = copy.deepcopy(playlist) # For undo command
            playlist.clear_playlist(playlist_name)
            if not self._undo:
                """For undo command"""
                self._lastCommand = 9
            else:
                self._undo = False

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self._allPlaylists.get(playlist_name.lower(), None)
        if playlist is None:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
        else:
            self._latest_deletedPlaylist = copy.deepcopy(playlist)  # For undo command
            del self._allPlaylists[playlist_name.lower()]
            print(f"Deleted playlist: {playlist_name}")

            if not self._undo:
                """For undo command"""
                self._lastCommand = 10 
            else:
                self._undo = False

    def show_filtered_videos(self, filtered_videos):
        count = 0
        searched_videos = {}
        for video in sorted(filtered_videos, key=operator.attrgetter('_title')):
            if video._flag is True:
                continue
            count += 1
            tags = " ".join(video._tags)
            print(f"  {count}) {video._title} ({video._video_id}) [{tags}]")
            searched_videos[str(count)] = video._video_id

        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        number = input("")
        if number in searched_videos:
            self.play_video(searched_videos[number])
        
        if self._undo:
                self._undo = False

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        all_videos = self._video_library.get_all_videos()
        filtered_videos = list(filter(lambda video: search_term.lower() in video._title.lower(), all_videos))

        if len(filtered_videos) > 0:
            print(f"Here are the results for {search_term}:")
            self.show_filtered_videos(filtered_videos)
        else:
            print(f"No search results for {search_term}")
        
        if self._undo:
                self._undo = False

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        all_videos = self._video_library.get_all_videos()
        filtered_videos = list(filter(lambda video: video_tag.lower() in " ".join(video._tags).lower(), all_videos))

        if len(filtered_videos) > 0:
            print(f"Here are the results for {video_tag}:")
            self.show_filtered_videos(filtered_videos)
        else:
            print(f"No search results for {video_tag}")
        
        if self._undo:
                self._undo = False

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video_to_be_flag = self._video_library.get_video(video_id)
        if video_to_be_flag == None:
            print("Cannot flag video: Video does not exist")
        else:
            if video_to_be_flag._flag is True:
                print("Cannot flag video: Video is already flagged")
            else:
                if self._currentVideo is not None and self._currentVideo._video_id is video_to_be_flag._video_id:
                    self.stop_video()
                reason = flag_reason if flag_reason != "" else "Not supplied"
                print(f"Successfully flagged video: {video_to_be_flag._title} (reason: {reason})")
                video_to_be_flag._flag, video_to_be_flag._flagreason = True, reason
                self.latest_flagged_video = [video_id, reason]
                if not self._undo:
                    """For undo command"""
                    self._lastCommand = 11 
                else:
                    self._undo = False

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video_to_be_unflag = self._video_library.get_video(video_id)
        if video_to_be_unflag == None:
            print("Cannot remove flag from video: Video does not exist")
        else:
            if video_to_be_unflag._flag is False:
                print("Cannot remove flag from video: Video is not flagged")
            else:
                print(f"Successfully removed flag from video: {video_to_be_unflag._title}")
                video_to_be_unflag._flag, video_to_be_unflag._flagreason = False, None
                self.latest_allowed_video = video_id
                if not self._undo:
                    """For undo command"""
                    self._lastCommand = 12 
                else:
                    self._undo = False
    
    """Extra features"""
    def play_playlist(self, playlist_name):
        """Play playlist"""
        playlist = self._allPlaylists.get(playlist_name.lower(), None)
        if playlist is None:
            """Check if playlist exists"""
            raise CommandException(f"Cannot play playlist {playlist_name}: Playlist does not exist")
        else:
            if not playlist._allVideos:
                """Check if playlist is empty"""
                raise CommandException(f"Cannot play playlist {playlist_name}: Playlist is empty")
            else:
                # if self._currentPlaylist is not None:
                #     print(f"Stop playing current playlist: {self._currentPlaylist._playlist_name}")

                print(f"Start playing playlist: {playlist_name}")
                self._currentPlaylist = playlist
                self.play_video(playlist._allVideos_id[0])
                if not self._undo:
                    """For undo command"""
                    self._lastCommand = 13 
                else:
                    self._undo = False
                
    def next_video(self):
        """Skip to next video in the playlist"""
        curent_playlist = self._currentPlaylist
        if curent_playlist is None:
            """Check if any playlist is currently playing""" 
            raise CommandException("Cannot skip to next video: No playlist is currently playing")
        else:
            if curent_playlist._playlist_position + 1 == len(curent_playlist._allVideos_id):
                """Check current position in the playlist"""
                raise CommandException("Cannot skip to next video: No next video available")
            else:
                position = curent_playlist._playlist_position + 1
                video_id = curent_playlist._allVideos_id[position]
                self.play_video(video_id)
                curent_playlist._playlist_position = position

    def show_current_playlist(self):
        """Show the name of the current playlist"""
        current_Playlist = self._currentPlaylist
        if current_Playlist is None:
            print("No playlist is currently playing")
        else:
            position = current_Playlist._playlist_position + 1
            print(f"Current playlist: {current_Playlist._playlist_name} - {position}/{len(current_Playlist._allVideos_id)}")
            self.show_playing()

    def show_video_rating(self, video_id):
        video = self._video_library.get_video(video_id)
        if video == None:
            raise CommandException("Cannot show video rating: Video does not exist")
        else:
            tags = " ".join(video._tags)
            video_info = f"{video._title} ({video._video_id}) [{tags}]"
            if video._flag is False and video._avg_rating != 0:
                print(f"  {video_info}, Rating: {video._avg_rating}")
            elif video._flag is False and video._avg_rating == 0:
                print(f"  {video_info} - Video is not yet rated.")
            else:
                if video._avg_rating == 0:
                    print(f"  {video_info} - Video is not yet rated and FLAGGED (reason: {video._flagreason})")
                else:
                    print(f"  {video_info}, Rating: {video._avg_rating} and FLAGGED (reason: {video._flagreason})")

    def rate_video(self, video_id, rating):
        """Rate specified video"""
        video = self._video_library.get_video(video_id)
        if video == None:
            raise CommandException("Cannot rate video: Video does not exist")
        else:
            if video._flag is True:
                raise CommandException(f"Cannot rate video: Video is currently flagged (reason: {video._flagreason})")
            else:
                try:
                    if not (1 <= float(rating) <= 5):
                        raise CommandException("Video rating can only be in a range of 1-5")
                except ValueError:
                    raise CommandException("Video rating can only be a number")

                video._rating.append(float(rating))
                print(f"Successfully rated video: {video._title}, Current average rating: {video.rating()}")

    def show_videos_by_rating(self):
        all_videos = self._video_library.get_all_videos()
        print("Here's a list of all available videos:")
        for video in sorted(all_videos, key=operator.attrgetter('_avg_rating'), reverse=True):
            self.show_video_rating(video._video_id)

    def undo(self):
        lastCommand = self._lastCommand
        if lastCommand is None:
            print("You have just started YT, there is no command to undo")
        elif lastCommand == 0:
            print("Cannot undo command consecutively and one has already been undone, please purchase YT premium to undo consecutively")
        else:
            self._undo, self._lastCommand = True, 0
            if lastCommand == 1:
                self.stop_video()
            elif lastCommand == 2:
                if self._previousPlaylist is not None:
                    self.play_playlist(self._previousPlaylist._playlist_name)
                else:
                    self.play_video(self._previousVideo._video_id)

            elif lastCommand == 3:
                self.stop_video()

            elif lastCommand == 4:
                self.continue_video()

            elif lastCommand == 5:
                self.pause_video()

            elif lastCommand == 6:
                self.delete_playlist(list(self._allPlaylists.keys())[-1])

            elif lastCommand == 7:
                self.remove_from_playlist(self._latest_video_added_to_playlist[0], self._latest_video_added_to_playlist[1])

            elif lastCommand == 8:
                self.add_to_playlist(self._latest_video_removed_from_playlist[0], self._latest_video_removed_from_playlist[1])

            elif lastCommand == 9:
                playlist = self._latest_clearedPlaylist
                playlist2 = self._allPlaylists[playlist._playlist_name.lower()]
                playlist2._allVideos = playlist._allVideos
                playlist2._allVideos_id = playlist._allVideos_id
                self._latest_clearedPlaylist = None
                print(f"Videos have been added back to playlist: {playlist2._playlist_name}")

            elif lastCommand == 10:
                playlist = self._latest_deletedPlaylist
                self.create_playlist(playlist._playlist_name)
                if playlist._allVideos_id:
                    playlist2 = self._allPlaylists[playlist._playlist_name.lower()]
                    playlist2._allVideos = playlist._allVideos
                    playlist2._allVideos_id = playlist._allVideos_id
                    print(f"Videos has been added back to playlist: {playlist2._playlist_name}")
    
                self._latest_deletedPlaylist = None

            elif lastCommand == 11:
                self.allow_video(self._latest_flagged_video[0])

            elif lastCommand == 12:
                self.flag_video(self.latest_allowed_video)

            elif lastCommand == 13:
                self.stop_video()