import { Image, StyleSheet, Button } from 'react-native';
import { ThemedText } from '../../components/ThemedText';
import { ThemedView } from '../../components/ThemedView';
import { ParallaxScrollView } from '../../components/ParallaxScrollView';

async function loginWithSpotify() {
  console.log('Logging in with Spotify');
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
          source={require('../../assets/images/4.png')}
          style={styles.tuneTimerLogo}
        />
      }>
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
  },
  stepContainer: {
    gap: 8,
    marginBottom: 8,
  },
  tuneTimerLogo: {
    height: 250,
    width: 400,
    resizeMode: 'cover',
  },
  text: {
    color: 'black',
  },
  headerText: {
    color: '#638C80',
  }
});
