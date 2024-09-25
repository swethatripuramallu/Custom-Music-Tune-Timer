import { Image, StyleSheet, Platform, Button, Linking } from 'react-native';

import { HelloWave } from '@/components/HelloWave';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { useState } from 'react';

import Config from 'react-native-config'

const baseUrl = Config.BASE_URL;
const [login, setLogin] = useState(false);

async function loginWithSpotify() {
   try {
       //const spotifyAuthUrl = `$(baseUrl)/login`; //couldn't get this to work
       const spotifyAuthUrl = 'http://10.0.2.15:5000/login'; //replace with your port number like mine, dont use locahost link
       Linking.openURL(spotifyAuthUrl);
    }
   catch(error) {
     console.error('Error logging in with Spotify:', error);
   }
}

export default function HomeScreen() {
  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#A1CEDC', dark: '#1D3D47' }}
      headerImage={
        <Image
          source={require('@/assets/images/partial-react-logo.png')}
          style={styles.reactLogo}
        />
      }>
      <ThemedView style={styles.titleContainer}>
        <ThemedText type="title">Welcome to Tune Timer!</ThemedText>
        <HelloWave />
      </ThemedView>
      <ThemedView style={styles.stepContainer}>
        <ThemedText type="subtitle">Step 1: Login with Spotify</ThemedText>
        <ThemedText>
          Click the button below to login with your Spotify account.
        </ThemedText>
        <Button title="Login with Spotify" onPress={loginWithSpotify} />
      </ThemedView>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  stepContainer: {
    gap: 8,
    marginBottom: 8,
  },
  reactLogo: {
    height: 178,
    width: 290,
    bottom: 0,
    left: 0,
    position: 'absolute',
  },
});
