import { Image, StyleSheet, Platform, Button, Linking } from 'react-native';

import { HelloWave } from '@/components/HelloWave';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { useState, useEffect } from 'react';

import * as dotenv from 'dotenv';
dotenv.config();

const baseUrl = process.env.BASE_URL;
const [login, setLogin] = useState(false);

async function loginWithSpotify() {
  // try {
  //   const response = await fetch('http://localhost:5000/login', {
  //     method: 'GET',
  //     redirect: 'follow',
  //   });
  //   const url = response.url;
  //   if(response.redirected) {
  //     // console.log('url', url);
  //     Linking.openURL(url);
  //   }
  // } catch(error) {
  //   console.error('Error logging in with Spotify:', error);
  // }
  // // Implement login with Spotify here
  // console.log('Login with Spotify');
  useEffect(() => {
    fetch(`${baseUrl}/login`).then(
      res => res.json()
    ).then(
      data => {
        setLogin(data)
        console.log(data)
      }
    )
  }, []);
  return {
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
