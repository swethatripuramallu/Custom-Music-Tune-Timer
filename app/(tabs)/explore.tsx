import Ionicons from '@expo/vector-icons/Ionicons';
import { StyleSheet, Image, Platform, Button, Linking } from 'react-native';
import { useState } from 'react';

import { Collapsible } from '@/components/Collapsible';
import { ExternalLink } from '@/components/ExternalLink';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { GestureHandlerRootView, TextInput } from 'react-native-gesture-handler';
import axios from 'axios';

export default function TabTwoScreen() {
  const [length, setLength] = useState('0');
  const [happy, setHappy] = useState(false);
  const [sad, setSad] = useState(false);
  const [dance, setDance] = useState(false);
  const [productive, setProductive] = useState(false);
  
  async function setHappyMood() {
    setHappy(true);
    console.log('Set Happy:', happy);
  }
  
  async function setSadMood() {
    setSad(true);
    console.log('Set Sad:', sad);
  }
  
  async function setDanceMood() {
    setDance(true);
    console.log('Set Dance:', dance);
  }
  
  async function setProductiveMood() {
    setProductive(true);
    console.log('Set Productive:', productive);
  }
  
  async function create() {
    console.log('Creating playlist');
    console.log('Length:', length);
    console.log('Happy:', happy);
    console.log('Sad:', sad);
    console.log('Dance:', dance);
    console.log('Productive:', productive);
    
    // Now, send the data to the backend
    const data = {
        length: length,
        happy: happy,
        sad: sad,
        dance: dance,
        productive: productive,
    };
    console.log(data)
  
    try {
        // Sending the state values to the Flask backend
        // const spotifyPlaylistUrl = 'http://10.0.2.15:5000/create-playlist' //swetha's url
        const spotifyPlaylistUrl = 'http://127.0.0.1:3002/create-playlist' //maggie's url
        // const spotifyPlaylistUrl = 'http://127.0.0.1:5001/create-playlist' //saniya's url
  
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
        // const spotifyDuration = 'http://10.0.2.15:5000/duration' //swetha's url
      const spotifyDuration = 'http://127.0.0.1:3002/duration' //maggie's url
        // const spotifyDuration = 'http://127.0.0.1:5001/duration' //saniya's url
  
        Linking.openURL(spotifyDuration);
  
    } catch (error) {
        console.log('oh no:', )
        console.error('Error sending data:', error);
    }
  }

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#A1CEDC', dark: '#1D3D47' }}
      headerImage={
      <Image
        source={require('@/assets/images/4.png')}
        style={styles.tuneTimerLogo}
      />
      }>
      <ThemedView>
        <ThemedText type="title">Create Custom Playlists</ThemedText>
        <ThemedText>Input your desired time and mood and create a custom playlist!</ThemedText>
        <GestureHandlerRootView>
          <TextInput value={length} onChangeText={setLength} placeholder="Enter length in minutes" /> 
          {/* (newLength) => setLength(newLength) */}
        </GestureHandlerRootView>
        <ThemedText>Click Mood Descriptors Below:</ThemedText>
        <Button title="Happy" onPress={setHappyMood}/>
        <Button title="Sad" onPress={setSadMood}/>
        <Button title="Dance" onPress={setDanceMood}/>
        <Button title="Productive" onPress={setProductiveMood}/>
        <ThemedText>Now, Create Your Playlist!</ThemedText>
        <Button title="Create Playlist!" onPress={create} />
      </ThemedView>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  headerImage: {
    color: '#808080',
    bottom: -90,
    left: -35,
    position: 'absolute',
  },
  titleContainer: {
    flexDirection: 'row',
    gap: 8,
  },
  tuneTimerLogo: {
    height: 250,
    width: 400,
    // bottom: 0,
    // left: 0,
    // position: 'absolute',
    resizeMode: 'cover',
  },
  text: {
    color: '#444545',
  }
});
