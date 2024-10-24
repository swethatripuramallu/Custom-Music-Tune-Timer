import { Image, StyleSheet, Platform, Button, Linking } from 'react-native';

import { MusicNote } from '@/components/MusicNote';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { useState } from 'react';

const [login, setLogin] = useState(false);

async function loginWithSpotify() {
   try {
      //  const spotifyAuthUrl = 'http://127.0.0.1:3002/login'; //maggie's localhost
      //  const spotifyAuthUrl = 'http://10.0.2.15:5000/login' //swetha's local host
      const spotifyAuthUrl = 'http://127.0.0.1:5001/login'; // saniya's localhost

       Linking.openURL(spotifyAuthUrl);
    }
   catch(error) {
     console.error('Error logging in with Spotify:', error);
   }
}

async function creatingPage() {
  console.log('Creating page');
}

export default function HomeScreen() {
  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#A1CEDC', dark: '#1D3D47' }}
      headerImage={
        <Image
          source={require('@/assets/images/4.png')}
          style={styles.tuneTimerLogo}
        />
      }>
      {/* <ThemedView style={styles.titleContainer}>
        <ThemedText type="title" style={styles.text}>Welcome to Tune Timer!</ThemedText>
        <MusicNote />
      </ThemedView> */}
      <ThemedView style={styles.stepContainer}>
        <ThemedText type="subtitle" style={styles.headerText}>Step 1: Login with Spotify</ThemedText>
        <ThemedText style={styles.text}>
          Click the button below to login with your Spotify account.
        </ThemedText>
        <Button title="Login with Spotify" onPress={loginWithSpotify} />
      </ThemedView>
      <ThemedView style={styles.stepContainer}>
        <ThemedText type="subtitle" style={styles.headerText}>Step 2: Begin Creating Custom Playlists</ThemedText>
        <ThemedText style={styles.text}>
          Input your desired time and mood and let Tune Timer create a custom playlist for you!
        </ThemedText>
        <Button title="Begin Creating" onPress={creatingPage} />
      </ThemedView>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    // backgroundColor: '#CEABB1',
  },
  stepContainer: {
    gap: 8,
    marginBottom: 8,
    // backgroundColor: '#CEABB1',
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
    color: 'black',
  },
  headerText: {
    color: '#638C80',
  }

});
