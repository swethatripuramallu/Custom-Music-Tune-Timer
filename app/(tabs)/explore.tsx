import { Ionicons } from '@expo/vector-icons';
import { StyleSheet, Button, Linking, TouchableOpacity, View, Image } from 'react-native';
import { useState } from 'react';
import Slider from '@react-native-community/slider'; 

import { Collapsible } from '@/components/Collapsible';
import { ExternalLink } from '@/components/ExternalLink';
import { ParallaxScrollView } from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { GestureHandlerRootView } from 'react-native-gesture-handler';

export default function TabTwoScreen() {
  const [length, setLength] = useState(0); 
  const [happy, setHappy] = useState(false);
  const [sad, setSad] = useState(false);
  const [dance, setDance] = useState(false);
  const [productive, setProductive] = useState(false);

  async function create() {
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
        Linking.openURL(result['playlist_url']);

    } catch (error) {
        console.error('Error sending data:', error);
    }
  }

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
            onValueChange={setLength} 
          />
          <ThemedText style={styles.sliderText}>
            {length} minutes
          </ThemedText>
        </View>

        <ThemedText style={styles.moodText}>Select Mood(s):</ThemedText>

        <TouchableOpacity style={styles.moodButton} onPress={() => setHappy(true)}>
          <ThemedText style={styles.buttonText}>Happy</ThemedText>
        </TouchableOpacity>
        <TouchableOpacity style={styles.moodButton} onPress={() => setSad(true)}>
          <ThemedText style={styles.buttonText}>Sad</ThemedText>
        </TouchableOpacity>
        <TouchableOpacity style={styles.moodButton} onPress={() => setDance(true)}>
          <ThemedText style={styles.buttonText}>Dance</ThemedText>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.moodButton, styles.lastMoodButton]} onPress={() => setProductive(true)}>
          <ThemedText style={styles.buttonText}>Productive</ThemedText>
        </TouchableOpacity>
        <ThemedText style={styles.createText}>Create Your Playlist Now!</ThemedText>
        <TouchableOpacity style={styles.createButton} onPress={create}>
          <ThemedText style={styles.buttonText}>Create!</ThemedText>
        </TouchableOpacity>
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
  headerImage: {
    color: '#808080',
    bottom: -90,
    left: -35,
    position: 'absolute',
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
});
