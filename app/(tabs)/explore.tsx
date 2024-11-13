import { StyleSheet, TextInput, Linking, TouchableOpacity, View, Image } from 'react-native';
import { useState } from 'react';
import Slider from '@react-native-community/slider'; 

import { ParallaxScrollView } from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { Link } from 'expo-router';

export default function ExploreScreen() {
  const [length, setLength] = useState<number>(0); 
  const [happy, setHappy] = useState(false);
  const [sad, setSad] = useState(false);
  const [dance, setDance] = useState(false);
  const [productive, setProductive] = useState(false);
  const [manualLength, setManualLength] = useState<string>(''); 

  const handleManualLengthChange = (text: string) => {
    const value = parseInt(text, 10);
    if (!isNaN(value) && value >= 1 && value <= 120) {
      setLength(value);
      setManualLength(text); 
    } else {
      setManualLength(text); 
    }
  };

  const setHappyMood = () => {
    setHappy(!happy);
    setSad(false);
    setDance(false);
    setProductive(false);
  };

  const setSadMood = () => {
    setHappy(false);
    setSad(!sad);
    setDance(false);
    setProductive(false);
  };

  const setDanceMood = () => {
    setHappy(false);
    setSad(false);
    setDance(!dance);
    setProductive(false);
  };

  const setProductiveMood = () => {
    setHappy(false);
    setSad(false);
    setDance(false);
    setProductive(!productive);
  };

  const createPlaylist = async () => {
    console.log('Creating playlist');
    console.log('Length:', length);
    console.log('Happy:', happy);
    console.log('Sad:', sad);
    console.log('Dance:', dance);
    console.log('Productive:', productive);
    
    const data = {
        length: length,
        happy: happy,
        sad: sad,
        dance: dance,
        productive: productive,
    };

    try {
        const spotifyPlaylistUrl = 'http://127.0.0.1:5001/create-playlist';

        const response = await fetch(spotifyPlaylistUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
          body: JSON.stringify(data),
        });

        const result = await response.json();
        console.log('Response from backend:', result);
        // Linking.openURL(result['playlist_url']);

    } catch (error) {
        console.error('Error sending data:', error);
    }
  };

  // Function to handle slider click/drag
  const handleSliderChange = (value: number) => {
    setLength(value);
    setManualLength(value.toString()); // Optionally update the manual input box when slider changes
  };

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#F1F0ED', dark: '#F1F0ED' }}
      headerImage={
        <ThemedView style={styles.container}>
          <Image
            source={require('@/assets/images/background.png')}
            style={styles.tuneTimerLogo}
          />
        </ThemedView>
      }
    >
      <ThemedView style={styles.container}>
        <ThemedText type="subtitle" style={styles.headerText}>
          Begin Creating!
        </ThemedText>
        <ThemedText style={styles.text}>
          Select Playlist Length!
        </ThemedText>

        <View style={styles.sliderContainer}>
          <Slider
            style={styles.slider}
            minimumValue={1}
            maximumValue={120}
            step={1}
            value={length}
            onValueChange={handleSliderChange} // Update length when slider is moved or clicked
            onSlidingComplete={handleSliderChange} // Set the length when user clicks anywhere on the slider
          />
          <ThemedText style={styles.sliderText}>
            {length} minutes
          </ThemedText>
        </View>

        <ThemedText style={styles.enterTimeText}>Or Enter Length (1-120 min):</ThemedText>
        <TextInput
          style={styles.input}
          value={manualLength}
          onChangeText={handleManualLengthChange}
          keyboardType="numeric"
          maxLength={3}
        />

        <ThemedText style={styles.moodText}>Select Mood(s):</ThemedText>

        <TouchableOpacity style={[styles.moodButton, happy && styles.pressedButton]} onPress={setHappyMood}>
          <ThemedText style={[styles.buttonText, happy && styles.pressedText]}>Happy</ThemedText>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.moodButton, sad && styles.pressedButton]} onPress={setSadMood}>
          <ThemedText style={[styles.buttonText, sad && styles.pressedText]}>Sad</ThemedText>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.moodButton, dance && styles.pressedButton]} onPress={setDanceMood}>
          <ThemedText style={[styles.buttonText, dance && styles.pressedText]}>Dance</ThemedText>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.moodButton, styles.lastMoodButton, productive && styles.pressedButton]} onPress={setProductiveMood}>
          <ThemedText style={[styles.buttonText, productive && styles.pressedText]}>Productive</ThemedText>
        </TouchableOpacity>

        <ThemedText style={styles.createText}>Create Your Playlist Now!</ThemedText>
        <Link href="./timer" asChild>
          <TouchableOpacity style={styles.createButton} onPress={createPlaylist}>
            <ThemedText style={styles.buttonText}>Create!</ThemedText>
          </TouchableOpacity>
        </Link>
      </ThemedView>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  tuneTimerLogo: {
    height: 250,
    width: 400,
    resizeMode: 'contain',
    borderRadius: 15,
  },
  container: {
    paddingHorizontal: 20,
    paddingVertical: 15,
    backgroundColor: 'transparent',
    alignItems: 'center',
    gap: 10,
  },
  headerText: {
    color: '#435f57',
    fontSize: 26,
    fontWeight: '700',
    marginBottom: 10,
    textAlign: 'center',
  },
  text: {
    color: '#444545',
    fontSize: 18,
    fontWeight: '500',
    textAlign: 'center',
    marginBottom: 15,
  },
  enterTimeText: {
    color: '#444545',
    fontSize: 16,
    fontWeight: '500',
    textAlign: 'center',
    marginBottom: 5,
  },
  sliderContainer: {
    width: '80%',
    marginBottom: 20,
    alignItems: 'center',
  },
  slider: {
    width: '100%',
    height: 40,
  },
  sliderText: {
    color: '#444545',
    fontSize: 16,
    fontWeight: '500',
    textAlign: 'center',
    marginTop: 10,
  },
  input: {
    width: '80%',
    height: 40,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 10,
    textAlign: 'center',
    fontSize: 18,
    marginBottom: 15,
  },
  moodText: {
    color: '#444545',
    fontSize: 18,
    fontWeight: '500',
    textAlign: 'center',
    marginBottom: 10,
  },
  moodButton: {
    backgroundColor: '#638C80',
    paddingVertical: 12,
    paddingHorizontal: 25,
    borderRadius: 25,
    alignItems: 'center',
    shadowColor: '#000',
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
  createText: {
    color: '#444545',
    fontSize: 18,
    fontWeight: '500',
    textAlign: 'center',
    marginBottom: 15,
  },
  createButton: {
    backgroundColor: '#638C80',
    paddingVertical: 12,
    paddingHorizontal: 25,
    borderRadius: 25,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 5 },
    shadowOpacity: 0.2,
    shadowRadius: 10,
    width: '70%',
    marginTop: 10,
  },
  lastMoodButton: {
    marginBottom: 20, 
  },
  pressedButton: {
    backgroundColor: 'white',
  },
  pressedText: {
    color: '#638C80',
    fontSize: 16,
    fontWeight: '600',
  }
});
