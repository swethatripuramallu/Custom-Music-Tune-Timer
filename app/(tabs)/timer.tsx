import React, { useEffect, useState } from 'react';
import { Text, StyleSheet, TouchableOpacity } from 'react-native';
import { CountdownCircleTimer } from 'react-native-countdown-circle-timer';
import { ThemedView } from '@/components/ThemedView'; 
import { ParallaxScrollView } from '@/components/ParallaxScrollView';

export default function ExploreScreen() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [length, setLength] = useState(0);
  const [reset, setReset] = useState(0);
  const [playlistStarted, setPlaylistStarted] = useState(false);
  const [likePlaylist, setLikePlaylist] = useState(true); 

  useEffect(() => {
    console.log('Timer duration updated:', length);
  }, [length]);

  const onTimerComplete = () => {
    console.log('Timer Complete!');
    playAlarm();
    if (likePlaylist) {
      console.log('Playlist liked');
    } else {
      console.log('Playlist disliked');
      deletePlaylist();
    }
  };

  async function playSound() {
    if (!playlistStarted) {
      try {
        const spotifyPlaylistUrl = 'http://127.0.0.1:5001/play';
        const response = await fetch(spotifyPlaylistUrl);
        const result = await response.json();
        const duration = parseInt(result, 10) / 1000; // Covnert to seconds
        console.log('Playlist duration:', duration);
        setLength(duration); // Update timer duration
        setIsPlaying(true);
      } catch (error) {
        console.error('Error playing playlist:', error);
      }
    } else {
      try {
        const spotifyPlaylistUrl = 'http://127.0.0.1:5001/resume';
        await fetch(spotifyPlaylistUrl);
      } catch (error) {
        console.error('Error resuming playlist:', error);
      }
    }
    setPlaylistStarted(true);
    setIsPlaying(true);
  }

  async function pauseSound() {
    setIsPlaying(false);
    try {
      const spotifyPlaylistUrl = 'http://127.0.0.1:5001/pause';
      await fetch(spotifyPlaylistUrl);
    } catch (error) {
      console.error('Error pausing playlist:', error);
    }
  }

  async function resetTimer() {
    try {
      const spotifyPlaylistUrl = 'http://127.0.0.1:5001/play';
      const response = await fetch(spotifyPlaylistUrl);
      const result = await response.json();
      const duration = parseInt(result, 10) / 1000; // Convert ms to seconds
      console.log('Playlist duration in seconds:', duration);
      setLength(duration); // Update length for timer
    } catch (error) {
      console.error('Error resetting playlist:', error);
    }
    setReset(reset + 1); // Trigger re-render
  }

  async function playAlarm() {
    try {
      const spotifyPlaylistUrl = 'http://127.0.0.1:5001/alarm';
      await fetch(spotifyPlaylistUrl);
    } catch (error) {
      console.error('Error playing alarm:', error);
    }
  }

  async function like() {
    console.log('Liked playlist');
    setLikePlaylist(true);
  }

  async function dislike() {
    console.log('Disliked playlist');
    setLikePlaylist(false);
  }

  async function deletePlaylist() {
    try {
      const spotifyPlaylistUrl = 'http://127.0.0.1:5001/delete';
      await fetch(spotifyPlaylistUrl);
    } catch (error) {
      console.error('Error deleting playlist:', error);
    }
  }

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#F1F0ED', dark: '#F1F0ED' }}
      headerImage={
        <ThemedView style={styles.container}>
          {/* This has been changed UI-vise on sg-timer-page-ui, can use that*/}
        </ThemedView>
      }
    >
      <ThemedView style={styles.container}>
        <Text style={styles.heading}>Begin Playing!</Text>
        <CountdownCircleTimer
          isPlaying={isPlaying}
          key={`${reset}-${length}`} // Ensure re-initialization of the timer
          duration={length} // Dynamically update the duration
          onComplete={onTimerComplete}
          size={250}
          strokeWidth={20}
          colors="#435f57"
          rotation="clockwise"
          trailColor="#e6e6e6"
          strokeLinecap="round"
        >
          {({ remainingTime }) => {
            const minutes = Math.floor(remainingTime / 60);
            const seconds = remainingTime % 60;
            return (
              <Text style={styles.timeText}>
                {minutes}:{seconds < 10 ? `0${seconds}` : seconds}
              </Text>
            );
          }}
        </CountdownCircleTimer>

        <TouchableOpacity style={styles.button} onPress={playSound}>
          <Text style={styles.buttonText}>Start</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.resetButton} onPress={pauseSound}>
          <Text style={styles.buttonText}>Stop</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.resetButton} onPress={resetTimer}>
          <Text style={styles.buttonText}>Reset</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.button} onPress={playAlarm}>
          <Text style={styles.buttonText}>Mute Alarm</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.button} onPress={like}>
          <Text style={styles.buttonText}>Like</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.button} onPress={dislike}>
          <Text style={styles.buttonText}>Dislike</Text>
        </TouchableOpacity>
      </ThemedView>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: 20,
    paddingVertical: 0,
    backgroundColor: 'transparent',
    alignItems: 'center',
    marginTop: 0,
  },
  heading: {
    fontSize: 24,
    fontWeight: '700',
    color: '#435f57', 
    marginBottom: 20, 
  },
  timeText: {
    fontSize: 40,
    color: '#638C80',
    fontWeight: '700',
  },
  button: {
    backgroundColor: '#638C80', 
    paddingVertical: 12,
    paddingHorizontal: 25,
    borderRadius: 25,
    alignItems: 'center',
    shadowColor: '#B0B7B3',
    shadowOffset: { width: 0, height: 5 },
    shadowOpacity: 0.2,
    shadowRadius: 10,
    width: '70%',
    marginTop: 20,
  },
  resetButton: {
    backgroundColor: '#638C80', 
    paddingVertical: 12,
    paddingHorizontal: 25,
    borderRadius: 25,
    alignItems: 'center',
    shadowColor: '#B0B7B3',
    shadowOffset: { width: 0, height: 5 },
    shadowOpacity: 0.2,
    shadowRadius: 10,
    width: '70%',
    marginTop: 10,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
});
