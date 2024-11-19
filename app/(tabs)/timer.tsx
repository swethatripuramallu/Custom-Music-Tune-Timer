import React, { useEffect, useState } from 'react';
import { Text, StyleSheet, TouchableOpacity } from 'react-native';
import { CountdownCircleTimer } from 'react-native-countdown-circle-timer';
import { ThemedView } from '@/components/ThemedView'; 
import { ParallaxScrollView } from '@/components/ParallaxScrollView';

export default function ExploreScreen() {
  const [isPlaying, setIsPlaying] = useState(false); // State to track if the timer is playing
  const [length, setLength] = useState(0);
  const [timeRemaining, setTimeRemaining] = useState(length);
  const [playlistStarted, setPlaylistStarted] = useState(false);
  const [reset, setReset] = useState(0);
  const [likePlaylist, setLikePlaylist] = useState(true); // automaticall saves playlist

  useEffect(() => {
    setTimeRemaining(length); // Reset time when length changes
  }, [length]);

  const onTimerComplete = () => {
    console.log('Timer Complete!');
    playAlarm();
    if(likePlaylist) {
      console.log('Playlist liked');
    }
    else {
      console.log('Playlist disliked');
      deletePlaylist();
    }
  };

  async function playSound() {
    if(!playlistStarted) {
      try {
        const spotifyPlaylistUrl = 'http://127.0.0.1:3002/play';
        const response = await fetch(spotifyPlaylistUrl);
        const result = await response.json();
        console.log('Response from backend:', result);
      } 
      catch (error) {
        console.error('Error playing playlist: ', error);
      }
      setLength(25); // Set timer length here
    }
    else {
      try {
        const spotifyPlaylistUrl = 'http://127.0.0.1:3002/resume';
        const response = await fetch(spotifyPlaylistUrl);
        const result = await response.json();
        console.log('Response from backend:', result);
      } 
      catch (error) {
        console.error('Error resume playing playlist: ', error);
      }
    }
    setPlaylistStarted(true);
    setIsPlaying(true); // start the timer
  }

  async function pauseSound() {
    setIsPlaying(false); // Stop the timer
    try {
      const spotifyPlaylistUrl = 'http://127.0.0.1:3002/pause';
      const response = await fetch(spotifyPlaylistUrl);
      const result = await response.json();
      console.log('Response from backend:', result);
    } 
    catch (error) {
      console.error('Error pausing playlist: ', error);
    }
  }

  async function resetTimer() {
    // reset playlist through backend
    try {
      const spotifyPlaylistUrl = 'http://127.0.0.1:3002/play';
      const response = await fetch(spotifyPlaylistUrl);

    } catch (error) {
      console.error('Error playing playlist: ', error);
    }

    setReset(reset + 1); // reset timer icon
  };

  async function playAlarm(){
    try {
      const spotifyPlaylistUrl = 'http://127.0.0.1:3002/alarm';
      const response = await fetch(spotifyPlaylistUrl);
    }
    catch (error) {
      console.error('Error playing alarm: ', error);
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
      const spotifyPlaylistUrl = 'http://127.0.0.1:3002/delete';
      const response = await fetch(spotifyPlaylistUrl);
    }
    catch (error) {
      console.error('Error deleting playlist: ', error);
    }
  }

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#F1F0ED', dark: '#F1F0ED' }}
      headerImage={
        <ThemedView style={styles.container}>
          {/* <Image
            source={require('@/assets/images/background.png')}
            style={styles.tuneTimerLogo}
          /> */}
        </ThemedView>
      }
    >
    <ThemedView style={styles.container}>
      <Text style={styles.heading}>Begin Playing!</Text>
      <CountdownCircleTimer
        isPlaying = {isPlaying}
        key={reset}
        duration={timeRemaining}  // length in seconds
        onComplete={onTimerComplete}
        size={250} 
        strokeWidth={20} 
        colors='#435f57'
        rotation="clockwise"
        trailColor="#e6e6e6" 
        strokeLinecap="round" 
      >
        {({ remainingTime }) => (
          <Text style={styles.timeText}>
            {remainingTime}s
          </Text>
        )}
      </CountdownCircleTimer>

      {/* Button to start/stop the timer */}
      <TouchableOpacity style={styles.button} onPress={playSound}>
        <Text style={styles.buttonText}>Start</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.resetButton} onPress={pauseSound}>
        <Text style={styles.buttonText}>Stop</Text>
      </TouchableOpacity>

      {/* Button to reset the timer */}
      <TouchableOpacity style={styles.resetButton} onPress={resetTimer}>
        <Text style={styles.buttonText}>Reset</Text>
      </TouchableOpacity>

      {/* Button to mute alarm */}
      <TouchableOpacity style={styles.button} onPress={playAlarm}>
        <Text style={styles.buttonText}>Mute Alarm</Text>
      </TouchableOpacity>

      {/* Button to like playlist */}
      <TouchableOpacity style={styles.button} onPress={like}>
        <Text style={styles.buttonText}>Like</Text>
      </TouchableOpacity>

      {/* Button to dislike playlist */}
      <TouchableOpacity style={styles.button} onPress={dislike}>
        <Text style={styles.buttonText}>Dislike</Text>
      </TouchableOpacity>
    </ThemedView>
    </ParallaxScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: 20,
    paddingVertical: 0,
    backgroundColor: 'transparent',
    alignItems: 'center',
    // gap: 10,
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
    color: '#fff',
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
  tuneTimerLogo: {
    height: 250,
    width: 400,
    resizeMode: 'contain',
    borderRadius: 15,
  },
});
