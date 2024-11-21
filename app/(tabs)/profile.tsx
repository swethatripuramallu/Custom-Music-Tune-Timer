import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, FlatList, StyleSheet, Image, TouchableOpacity, Alert, Modal } from 'react-native';
import { ParallaxScrollView } from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { Link } from 'expo-router';
import { useFocusEffect } from '@react-navigation/native';

const PORT = 5000; // set port number

const ProfilePage: React.FC = () => {
  const [mostRecentPlaylist, setMostRecentPlaylist] = useState<{ name: string; playlist_modified: string | null; message?: string } | null>(null);
  const [error, setError] = useState<string | null>(null);
  // const [message, setMessage] = useState<string | null>(null);
  // const [isModalVisible, setIsModalVisible] = useState(false); // Modal state

  const fetchMostRecentPlaylist = async () => {
    try {
      const most_recent_playlist = `http://127.0.0.1:${PORT}/most-recent-playlist`;
      const response = await fetch(most_recent_playlist);

      if (!response.ok) {
        const errorData = await response.json();
        // Handle "Playlist not found" explicitly
        if (response.status === 404 && errorData.error === "Playlist not found.") {
          setError('No recent Tune Timer playlists available.');
          setMostRecentPlaylist(null); // Clear any existing playlist data
          return; // Exit the function
        } else {
          throw new Error(errorData.error || 'Unknown error occurred');
        }
      }
  
      const result = await response.json();
      console.log('Response from backend:', result);
  
      if (result && result.name && result.playlist_modified) {
        setMostRecentPlaylist(result);
        setError(null); // Clear any errors
      } else {
        setMostRecentPlaylist(null);
        setError('No valid playlist data available.');
      }
    } catch (error: any) {
      console.error('Error retrieving most recent playlist:', error.message);
      setError('Could not fetch the most recent playlist.');
      setMostRecentPlaylist(null);
    }
  };

  const deletePlaylist = async () => {
    try {
      const delete_endpoint = `http://127.0.0.1:${PORT}/delete`;

      const response = await fetch(delete_endpoint);

      if (!response.ok) {
        throw new Error('Failed to delete the playlist');
      }

      const result = await response.json();
      console.log('Response from backend:', result);

      // setMessage('The playlist has been deleted.');

      await fetchMostRecentPlaylist();
    } catch (error: any) {
      console.error('Error deleting playlist:', error.message);
      setError('Could not delete the playlist.');
    }
  };

  // const deletePlaylist = async () => {
  //   try {
  //     const delete_endpoint = `http://127.0.0.1:${PORT}/delete`;

  //     const response = await fetch(delete_endpoint);

  //     if (!response.ok) {
  //       throw new Error('Failed to delete the playlist');
  //     }

  //     const result = await response.json();
  //     console.log('Response from backend:', result);

  //     // setMessage('The playlist has been deleted.');
  //     // Show success message after deletion
  //     // Alert.alert('Playlist Deleted', 'The playlist has been successfully deleted.', [
  //     //   {
  //     //     text: 'OK',
  //     //     onPress: async () => {
  //     //       await fetchMostRecentPlaylist(); // Refresh playlist data after deletion
  //     //     },
  //     //   },
  //     // ]);
  //     setIsModalVisible(true); // Show modal after deletion
  //     await fetchMostRecentPlaylist();
  //   } catch (error: any) {
  //     console.error('Error deleting playlist:', error.message);
  //     setError('Could not delete the playlist.');
  //   }

  // };
  
  useFocusEffect(
    useCallback(() => {
      fetchMostRecentPlaylist();
    }, [])
  );

  const formatDate = (isoDate: string) => {
    const date = new Date(isoDate);
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      timeZone: 'America/New_York',
      timeZoneName: 'short',
    }).format(date);
  };

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

        <Link href="/explore" asChild>
          <TouchableOpacity style={styles.button}>
            <ThemedText style={styles.buttonText}>Create New Playlist</ThemedText>
          </TouchableOpacity>
        </Link>

        <View style={styles.recentPlaylistContainer}>
          <ThemedText style={styles.recentPlaylistTitle}>Most Recent Playlist:</ThemedText>
          {error ? (
            <Text style={styles.noPlaylistText}>No recent Tune Timer playlists available.</Text>
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

              <View style={styles.confirmationContainer}>
                <ThemedText style={styles.confirmationText}>
                  Keep this playlist?
                </ThemedText>
                <View style={styles.buttonRow}>
                  <TouchableOpacity style={styles.yesButton} onPress={() => Alert.alert('Saved', 'Playlist has been successfully saved')}>
                    <Text style={styles.buttonText}>Yes</Text>
                  </TouchableOpacity>
                  {/* <TouchableOpacity style={styles.noButton} onPress={(deletePlaylist) => Alert.alert('Playlist deleted.')}> */}
                  <TouchableOpacity
                        style={styles.noButton}
                        onPress={async () => {
                          await deletePlaylist(); // Call deletePlaylist function
                          Alert.alert('Deleted', 'Playlist has been succesfully deleted'); // Show success message
                        }}
                      >
                    <Text style={styles.buttonText}>No</Text>
                  </TouchableOpacity>
                </View>
              </View>
            </View>
          ) : (
            <Text style={styles.loadingText}>Loading playlist information...</Text>
          )}
        </View>

        {/*message && <Text style={styles.successMessage}>{message}</Text>*/}
         {/* Modal for success message */}
         {/* <Modal
          animationType="slide"
          transparent={true}
          visible={isModalVisible}
          onRequestClose={() => setIsModalVisible(false)} // Close modal on back press
        >
          <View style={styles.modalContainer}>
            <View style={styles.modalContent}>
              <Text style={styles.modalText}>Playlist has been deleted.</Text>
              <TouchableOpacity onPress={() => setIsModalVisible(false)} style={styles.closeButton}>
                <Text style={styles.buttonText}>OK</Text>
              </TouchableOpacity>
            </View>
          </View>
        </Modal> */}

      </ThemedView>
    </ParallaxScrollView>
  );
};

const styles = StyleSheet.create({
  modalContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  modalContent: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 10,
    alignItems: 'center',
    width: 300,
  },
  modalText: {
    fontSize: 18,
    marginBottom: 15,
    textAlign: 'center',
  },
  closeButton: {
    backgroundColor: '#638C80',
    padding: 12,
    borderRadius: 10,
    width: 100,
    alignItems: 'center',
  },
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
    padding: 5,
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
    borderRadius: 15,
    alignItems: 'center',
    padding: 15,  
    maxWidth: 350,  
  },
  confirmationText: {
    fontSize: 16,
    color: '#435f57',
    fontWeight: 'bold',
    marginBottom: 15,
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
    backgroundColor: '#638C80',
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
