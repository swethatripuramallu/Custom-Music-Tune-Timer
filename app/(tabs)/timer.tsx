import React, { useEffect, useState } from 'react';
import { Text, StyleSheet, TouchableOpacity } from 'react-native';
import { CountdownCircleTimer } from 'react-native-countdown-circle-timer';
import { useTimer } from '../timerlength'; 
import { ThemedView } from '@/components/ThemedView'; 

const Timer: React.FC = () => {
  const { length } = useTimer(); // Get the length from the context - WIP
  const [timeRemaining, setTimeRemaining] = useState(length);
  const [isPlaying, setIsPlaying] = useState(false); // State to track if the timer is playing

  useEffect(() => {
    setTimeRemaining(length); // Reset time when length changes
  }, [length]);

  const onTimerComplete = () => {
    console.log('Timer Complete!');
  };

  async function playSound() {
    toggleTimer();
    try {
      const spotifyPlaylistUrl = 'http://127.0.0.1:3002/play';

      const response = await fetch(spotifyPlaylistUrl);

      // const result = await response.json();
      // console.log('Response from backend:', result);
      // Linking.openURL(result['playlist_url']);

    } catch (error) {
      console.error('Error playing playlist: ', error);
    }
  }

  const toggleTimer = () => {
    setIsPlaying((prev) => !prev); // Toggle the timer state between playing and paused
  };

  const resetTimer = () => {
    setIsPlaying(false); // Stop the timer
    setTimeRemaining(length); // Reset the time
  };

  return (
    <ThemedView style={styles.container}>
      {/* Heading */}
      <Text style={styles.heading}>Begin Playing!</Text>

      <CountdownCircleTimer
        isPlaying={isPlaying}
        duration={length} 
        initialRemainingTime={timeRemaining} 
        onComplete={onTimerComplete}
        size={250} 
        strokeWidth={20} 
        colors='#435f57'
        rotation="counterclockwise"
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
        <Text style={styles.buttonText}>
          {isPlaying ? 'Stop' : 'Start'}
        </Text>
      </TouchableOpacity>

      {/* Button to reset the timer */}
      <TouchableOpacity style={styles.resetButton} onPress={resetTimer}>
        <Text style={styles.buttonText}>Reset</Text>
      </TouchableOpacity>
    </ThemedView>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: 20,
    paddingVertical: 15,
    backgroundColor: 'transparent',
    alignItems: 'center',
    gap: 10,
    marginTop: 60,
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
});

export default Timer;
