import React, {useState, useEffect, useCallback} from 'react';
import { View, Text, FlatList, StyleSheet, Image, TouchableOpacity, Alert } from 'react-native';
import { ParallaxScrollView } from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { Link } from 'expo-router';
import { useFocusEffect } from '@react-navigation/native';



// Example playlist data
const ProfilePage: React.FC = () => {
  const [mostRecentPlaylist, setMostRecentPlaylist] = useState<{ name: string; playlist_modified: string | null; message?: string } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  // Fetch the most recent playlist
  const fetchMostRecentPlaylist = async () => {
    try {
      const most_recent_playlist = 'http://127.0.0.1:5000/most-recent-playlist';
      const response = await fetch(most_recent_playlist);
  
      if (!response.ok) {
        const errorData = await response.json();
        if (errorData.error === "Playlist not found.") {
          setError(null); // Clear the error message
          setMostRecentPlaylist(null); // No playlist found
        } else {
          throw new Error(errorData.error || 'Unknown error occurred');
        }
      } else {
        const result = await response.json();
        console.log('Response from backend:', result);
  
        if (result && result.name && result.playlist_modified) {
          setMostRecentPlaylist(result);
          setError(null);
        } else {
          setMostRecentPlaylist(null);
          setError('No valid playlist data available.');
        }
      }
    } catch (error: any) {
      console.error('Error retrieving most recent playlist:', error.message);
      setError('Could not fetch the most recent playlist.');
      setMostRecentPlaylist(null);
    }
  };

  // Delete the playlist
  const deletePlaylist = async () => {
    try {
      const delete_endpoint = 'http://127.0.0.1:5000/delete';
      const response = await fetch(delete_endpoint);

      if (!response.ok) {
        throw new Error('Failed to delete the playlist');
      }

      const result = await response.json();
      console.log('Response from backend:', result);

      setMessage('The playlist has been deleted.');

      // Fetch the most recent playlist after deletion
      await fetchMostRecentPlaylist();
    } catch (error: any) {
      console.error('Error deleting playlist:', error.message);
      setError('Could not delete the playlist.');
    }
  };

  useFocusEffect(
    useCallback(() => {
      fetchMostRecentPlaylist();
    }, [])
  );

  const formatDate = (isoDate) => {
    const date = new Date(isoDate);

  return new Intl.DateTimeFormat('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    timeZone: 'America/New_York',
    timeZoneName: 'short',
  }).format(date);
};

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
            <Text style={styles.loadingText}>No recent Tune Timer playlists available.</Text>
          ) : mostRecentPlaylist ? (
            <View style={styles.recentPlaylistItem}>
              <Text style={styles.itemTitle}>Name:</Text>
              <Text style={styles.itemValue}>{mostRecentPlaylist.name}</Text>
              <Text style={styles.itemTitle}>Modified Date:</Text>
              {mostRecentPlaylist.playlist_modified ? (
                <Text style={styles.itemValue}>{formatDate(mostRecentPlaylist.playlist_modified)}</Text>
              ) : (
                <Text style={styles.errorText}>This playlist has no tracks.</Text>
              )}

              {/* Yes/No Buttons */}
              <View style={styles.confirmationContainer}>
                <ThemedText style={styles.confirmationText}>Do you want to keep this playlist?</ThemedText>
                <View style={styles.buttonRow}>
                  <TouchableOpacity style={styles.yesButton} onPress={() => Alert.alert('Playlist kept.')}>
                    <Text style={styles.buttonText}>Yes</Text>
                  </TouchableOpacity>
                  <TouchableOpacity style={styles.noButton} onPress={deletePlaylist}>
                    <Text style={styles.buttonText}>No</Text>
                  </TouchableOpacity>
                </View>
              </View>
            </View>
          ) : (
            <Text style={styles.loadingText}>No recent Tune Timer playlists available.</Text>
          )}
        </View>

        {/* Success or Error Message */}
        {message && <Text style={styles.successMessage}>{message}</Text>}
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

  confirmationContainer: {
    marginTop: 20,
    alignItems: 'center',
  },
  confirmationText: {
    fontSize: 16,
    color: '#435f57',
    marginBottom: 10,
  },
  buttonRow: {
    flexDirection: 'row',
    gap: 15,
  },
  yesButton: {
    backgroundColor: '#638C80',
    padding: 12,
    borderRadius: 25,
    width: 100,
    alignItems: 'center',
  },
  noButton: {
    backgroundColor: '#d9534f',
    padding: 12,
    borderRadius: 25,
    width: 100,
    alignItems: 'center',
  },
  successMessage: {
    marginTop: 15,
    fontSize: 14,
    color: 'green',
  },
});

export default ProfilePage;
