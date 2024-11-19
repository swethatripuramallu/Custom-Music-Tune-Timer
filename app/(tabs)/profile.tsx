import React, {useState, useEffect} from 'react';
import { View, Text, FlatList, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { ParallaxScrollView } from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { Link } from 'expo-router';


// Example playlist data
const ProfilePage: React.FC = () => {

  const [mostRecentPlaylist, setMostRecentPlaylist] = useState(null);
  const [error, setError] = useState<string | null>(null);

  // Fetch the most recent playlist
  useEffect(() => {
    const fetchMostRecentPlaylist = async () => {
      try {
        const most_recent_playlist = 'http://127.0.0.1:5000/most-recent-playlist'; // Change the URL as needed
        const response = await fetch(most_recent_playlist);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const result = await response.json();
        console.log('Response from backend:', result);
        setMostRecentPlaylist(result); // Assuming `result` contains the playlist data
      } catch (error) {
        console.error('Error retrieving most recent playlist: ', error);
        setError('Could not fetch the most recent playlist.');
      }
    };

    fetchMostRecentPlaylist();
  }, []);

  // Render each item in the profile data
  const renderItem = ({ item }: { item: { title: string; value: string } }) => (
    <View style={styles.profileItem}>
      <Text style={styles.itemTitle}>{item.title}:</Text>
      <Text style={styles.itemValue}>{item.value}</Text>
    </View>
  );

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#F1F0ED', dark: '#F1F0ED' }}
      headerImage={
        <ThemedView style={styles.logoContainer}>
          <Image
            source={require('@/assets/images/blank.png')}
            style={styles.tuneTimerLogo}
          />
        </ThemedView>
      }
    >
      <ThemedView style={styles.container}>
        <ThemedText type="subtitle" style={styles.headerText}>
          Profile
        </ThemedText>

        {/* Navigate to other pages */}
        <Link href="/explore" asChild>
          <TouchableOpacity style={styles.button}>
            <ThemedText style={styles.buttonText}>Create New Playlist</ThemedText>
          </TouchableOpacity>
        </Link>

         {/* Most Recent Playlist */}
        <View style={styles.recentPlaylistContainer}>
          <ThemedText style={styles.recentPlaylistTitle}>Most Recent Playlist:</ThemedText>
          {error ? (
            <Text style={styles.errorText}>{error}</Text>
          ) : mostRecentPlaylist ? (
            <View style={styles.recentPlaylistItem}>
              <Text style={styles.itemTitle}>{mostRecentPlaylist}</Text>
              <Text style={styles.itemValue}>{mostRecentPlaylist}</Text>
            </View>
          ) : (
            <Text style={styles.loadingText}>No recent tune timer playlists</Text>
          )}
        </View>

      </ThemedView>
    </ParallaxScrollView>
  );
};

const styles = StyleSheet.create({
  logoContainer: {
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 20,
  },
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
  profileItem: {
    marginBottom: 15,
    padding: 10,
    backgroundColor: '#fff',
    borderRadius: 5,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowOffset: { width: 0, height: 1 },
    shadowRadius: 3,
    elevation: 3,
    width: '100%',
  },

  recentPlaylistContainer: {
    marginTop: 20,
    width: '100%',
    alignItems: 'center',
  },
  recentPlaylistTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#435f57',
    marginBottom: 10,
  },
  recentPlaylistItem: {
    padding: 10,
    backgroundColor: '#fff',
    borderRadius: 5,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowOffset: { width: 0, height: 1 },
    shadowRadius: 3,
    elevation: 3,
    width: '100%',
    maxWidth: 300,
    alignItems: 'center',
  },

  noPlaylistText: {
    fontSize: 14,
    color: '#999',
    marginTop: 10,
  },

  itemTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  itemValue: {
    fontSize: 14,
    color: '#666',
  },
  errorText: {
    fontSize: 14,
    color: 'red',
    marginTop: 10,
  },
  loadingText: {
    fontSize: 14,
    color: '#999',
    marginTop: 10,
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
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
});

export default ProfilePage;
