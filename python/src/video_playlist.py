"""A video playlist class."""

class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, playlist_name):
        """Playlist constructor."""
        self._playlist_name = playlist_name
        self._allVideos = {}
        self._allVideos_id = []
        self._playlist_position = 0

    def add_video(self, playlist_name, video):
        if video._video_id in self._allVideos:
            """ Check if video exists in the playlist"""
            print(f"Cannot add video to {playlist_name}: Video already added")
        else:
            self._allVideos[video._video_id] = video
            self._allVideos_id.append(video._video_id)
            print(f"Added video to {playlist_name}: {video._title}")
    
    def show_videos(self, playlist_name):
        print(f"Showing playlist: {playlist_name}")
        if len(self._allVideos) == 0:
            print("  No videos here yet")
        else:
            for _, video in self._allVideos.items():
                tags = " ".join(video._tags) 
                video_info = f"{video._title} ({video._video_id}) [{tags}]"
                if video._flag is False:
                    print(f"  {video_info}")
                else:
                    print(f"  {video_info} - FLAGGED (reason: {video._flagreason})")
    
    def remove_video(self,  playlist_name, video_id):
        video = self._allVideos.get(video_id, None)
        if video is None:
            print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
        else:
            del self._allVideos[video._video_id]
            self._allVideos_id.remove(video._video_id)
            print(f"Removed video from {playlist_name}: {video._title}")

    def clear_playlist(self, playlist_name):
        """Remove all videos from playlist"""
        self._allVideos.clear()
        self._allVideos_id.clear()
        self._playlist_position = 0
        print(f"Successfully removed all videos from {playlist_name}")