<template>
  <div>
    <iframe v-if="formattedVideoUrl" :src="formattedVideoUrl" frameborder="0" allowfullscreen class="video-player-iframe" id="player"></iframe>
  </div>
</template>

<script>
/* global YT */

export default {
  name: 'VideoPlayer',
  props: {
    videoUrl: {
      type: String,
      required: true,
    },
  },
  computed: {
    // Format the YouTube video URL for embedding
    formattedVideoUrl() {
      const videoId = this.getVideoIdFromUrl(this.videoUrl);
      return videoId ? `https://www.youtube.com/embed/${videoId}` : null;
    },
  },
  methods: {
    loadYouTubePlayer() {
      const tag = document.createElement('script');
      tag.src = 'https://www.youtube.com/iframe_api';
      const firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

      window.onYouTubeIframeAPIReady = () => {
        new YT.Player('player', {
          videoId: this.videoUrl,  // Ensure this is passed correctly as videoId
          events: {
            onReady: this.onPlayerReady,
            onError: this.onPlayerError,
          },
        });
      };
    },
    getVideoIdFromUrl(url) {
      // Use the URL API to extract the video ID
      try {
        const urlObj = new URL(url);
        const videoId = urlObj.searchParams.get('v');
        return videoId ? videoId : null;
      } catch (e) {
        console.error('Error parsing video URL:', e);
        return null;
      }
    },
    onPlayerReady(event) {
      event.target.playVideo();
    },
    onPlayerError(event) {
      console.error('Error with YouTube Player:', event.data);
    },
  },
};
</script>

<style scoped>
#player {
  width: 112rem;
  height: 63rem;
}
</style>
