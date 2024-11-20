import React, { useEffect, useState } from 'react';
import { Text, StyleSheet, TouchableOpacity, View, Image } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome';
import { CountdownCircleTimer } from 'react-native-countdown-circle-timer';
import { ThemedView } from '@/components/ThemedView'; 
import { ParallaxScrollView } from '@/components/ParallaxScrollView';

const PORT = 5001; // set port number

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
        const spotifyPlaylistUrl = `http://127.0.0.1:${PORT}/play`;

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
        const spotifyPlaylistUrl = `http://127.0.0.1:${PORT}/resume`;
        const response = await fetch(spotifyPlaylistUrl);
        const result = await response.json();
        console.log('Response from backend:', result);
        setIsPlaying(true);
      } catch (error) {
        console.error('Error resuming playlist: ', error);
      }
    }
    setPlaylistStarted(true);
    // setIsPlaying(true);
  }

  async function pauseSound() {
    setIsPlaying(false);
    try {
      const spotifyPlaylistUrl = `http://127.0.0.1:${PORT}/pause`;
      const response = await fetch(spotifyPlaylistUrl);
      const result = await response.json();
      console.log('Response from backend:', result);
    } catch (error) {
      console.error('Error pausing playlist: ', error);
    }
  }

  async function resetTimer() {
    try {
      const spotifyPlaylistUrl = `http://127.0.0.1:${PORT}/play`;
      const response = await fetch(spotifyPlaylistUrl);
      const result = await response.json();
      const duration = parseInt(result, 10) / 1000; // Convert ms to seconds
      console.log('Playlist duration in seconds:', duration);
      setLength(duration); // Update length for timer
    } catch (error) {
      console.error('Error resetting playlist:', error);
    }
    setIsPlaying(true);
    setReset(reset + 1); // Trigger re-render
  }

  async function playAlarm() {
    try {
      const spotifyPlaylistUrl = `http://127.0.0.1:${PORT}/alarm`;

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
      const spotifyPlaylistUrl = `http://127.0.0.1:${PORT}/delete`;
      const response = await fetch(spotifyPlaylistUrl);
    }
    catch (error) {
      console.error('Error deleting playlist: ', error);
    }
  }

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ dark: "#F1F0ED", light: "#F1F0ED" }}
      headerImage={(
        <ThemedView style={styles.logoContainer}>
          <Image
            source={require('@/assets/images/blank.png')}
            style={styles.tuneTimerLogo}
          />
        </ThemedView>
      )}
      // headerImage={<Image source={require('@/assets/images/blank.png')} style={styles.headerImage} />} // Header image here
    >
      <ThemedView style={styles.container}>
        <Text style={styles.heading}>Begin Playing!</Text>
        <CountdownCircleTimer
          isPlaying={isPlaying}
          key={reset}
          duration={length}
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

        {/* Timer Controls */}
        <View style={styles.row}>
          <TouchableOpacity style={styles.button} onPress={playSound}>
            <Text style={styles.buttonText}>Start</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.button} onPress={resetTimer}>
            <Text style={styles.buttonText}>Reset</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.button} onPress={pauseSound}>
            <Text style={styles.buttonText}>Stop</Text>
          </TouchableOpacity>
        </View>

        {/* Playlist Actions */}
        <View style={styles.iconRow}>
          <TouchableOpacity style={styles.iconButton} onPress={like}>
            <Icon name="thumbs-up" size={24} color="white" />
          </TouchableOpacity>
          <TouchableOpacity style={styles.iconButton} onPress={dislike}>
            <Icon name="thumbs-down" size={24} color="white" />
          </TouchableOpacity>
        </View>
      </ThemedView>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: 20,
    alignItems: 'center',
    backgroundColor: 'transparent',
  },
  logoContainer: {
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 20,
  },
  tuneTimerLogo: {
    height: 250,
    width: 400,
    resizeMode: 'contain',
    borderRadius: 15,
  },
  heading: {
    fontSize: 30,
    fontWeight: '700',
    color: '#435f57',
    marginBottom: 20,
  },
  timeText: {
    fontSize: 40,
    color: '#638C80',
    fontWeight: '700',
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginVertical: 15,
    width: '100%',
  },
  button: {
    backgroundColor: '#638C80',
    paddingVertical: 15,
    borderRadius: 25,
    alignItems: 'center',
    width: '30%',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  iconRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 15,
    width: '50%',
  },
  iconButton: {
    backgroundColor: '#638C80',
    borderRadius: 50,
    padding: 17,
    alignItems: 'center',
    justifyContent: 'center',
  },
  headerImage: {
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 20,
    },
  },
);
