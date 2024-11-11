import React, { useState, useEffect } from 'react';
import { Text, View, StyleSheet } from 'react-native';
import { CountdownCircleTimer } from 'react-native-countdown-circle-timer';
import { useTimer } from '../timerlength'; // Access the global timer length from context

const Timer: React.FC = () => {
  const { length } = useTimer(); // Get the length from the context
  const [timeRemaining, setTimeRemaining] = useState(length);

  useEffect(() => {
    setTimeRemaining(length); // Reset time remaining whenever the `length` changes

    if (length <= 0) return; // Stop if length is 0
    const timerId = setInterval(() => {
      setTimeRemaining((prev) => prev - 1); // Decrease the time remaining
    }, 1000);

    return () => clearInterval(timerId); // Clean up the interval when the component unmounts or length changes
  }, [length]);

  const onTimerComplete = () => {
    console.log('Timer Complete!');
  };

  return (
    <View style={styles.timer}>
      <CountdownCircleTimer
        isPlaying
        duration={length} // Use the length from context to set the timer duration
        initialRemainingTime={timeRemaining}
        onComplete={onTimerComplete}
        size={200}
        strokeWidth={10}
        colors="#FF6347"
      >
        {({ remainingTime }) => (
          <Text style={{ fontSize: 30 }}>
            {remainingTime}s
          </Text>
        )}
      </CountdownCircleTimer>
    </View>
  );
};

const styles = StyleSheet.create({
  timer: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 2,
    borderColor: '#fff',
    padding: 20,
  },
});

export default Timer;
