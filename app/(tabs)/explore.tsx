import Ionicons from '@expo/vector-icons/Ionicons';
import { StyleSheet, Image, Platform, Button } from 'react-native';
import { useState, useEffect } from 'react';

import { Collapsible } from '@/components/Collapsible';
import { ExternalLink } from '@/components/ExternalLink';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { GestureHandlerRootView, TextInput } from 'react-native-gesture-handler';

const [length, onChangeLength] = useState('0');
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
}

export default function TabTwoScreen() {
  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#D0D0D0', dark: '#353636' }}
      headerImage={<Ionicons size={310} name="code-slash" style={styles.headerImage} />}>
      <ThemedView>
        <ThemedText type="title">Create Custom Playlists</ThemedText>
        <ThemedText>Input your desired time and mood and let Tune Timer create a custom playlist for you!</ThemedText>
        <GestureHandlerRootView>
          <TextInput value={length} onChangeText={onChangeLength} placeholder="Enter length" />
        </GestureHandlerRootView>
        <ThemedText>Select Mood Descriptors Below:</ThemedText>
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
  text: {
    color: '#444545',
  }
});
