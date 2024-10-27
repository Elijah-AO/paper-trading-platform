// src/screens/SearchScreen.tsx
import React, { useState } from 'react';
import { View, FlatList, Text, Pressable } from 'react-native';
import { Box, Input, Icon } from 'native-base';
import { ScrollView, VStack, HStack, Button, Center } from 'native-base';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation, NavigationProp } from '@react-navigation/native';
import { RootStackParamList } from '../navigation/types';

const SearchScreen = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [results, setResults] = useState<{ id: string; symbol: string; name: string }[]>([]);
    const navigation = useNavigation<NavigationProp<RootStackParamList>>();

    const navigateToHome = () => {
        navigation.navigate('Dashboard');
      };
    
      const navigateToSearch = () => {
        navigation.navigate('Search');
      };

    const handleSearch = async (query: string) => {
        setSearchQuery(query);

        if (query) {
            try {
                const response = await fetch(`http://localhost:5000/api/stocks/search?query=${query}`);
                
                if (!response.ok) {
                    throw new Error('Failed to fetch results');
                }

                const data = await response.json();
                setResults(data);
            } catch (error) {
                console.error(error);
                setResults([]);
            }
        } else {
            setResults([]); // Clear results if query is empty
        }
    };

    const handleStockPress = (stock: { id: string; symbol: string; name: string }) => {
        navigation.navigate('Stock', {
            stockId: stock.id,
            symbol: stock.symbol,
            name: stock.name,
        });
    };

    return (
        <VStack className="flex-1 bg-white">
        <View style={{ flex: 1, padding: 16, backgroundColor: 'white' }}>
            <Box style={{ marginBottom: 16 }}>
                <Input
                    placeholder="Search"
                    value={searchQuery}
                    onChangeText={handleSearch}
                    InputLeftElement={
                        <Icon as={<Ionicons name="search" />} size={5} ml="2" color="gray.400" />
                    }
                    style={{ borderWidth: 1, borderRadius: 8, padding: 8 }}
                />
            </Box>
            <FlatList
                data={results}
                keyExtractor={(item) => item.id}
                renderItem={({ item }) => (
                    <Pressable onPress={() => handleStockPress(item)}>
                        <Box style={{ padding: 16, borderBottomWidth: 1, borderBottomColor: 'gray.200' }}>
                            <Text style={{ fontWeight: 'bold' }}>{item.symbol}</Text>
                            <Text>{item.name}</Text>
                        </Box>
                    </Pressable>
                )}
                ListEmptyComponent={<Text style={{ textAlign: 'center', color: 'gray.500' }}>No results found</Text>}
                contentContainerStyle={{ paddingBottom: 16 }}
            />
                  {/* Footer */}
      <HStack className="border-t border-gray-300 bg-gray-100" style={{ width: '100%' }}>
        <Button variant="ghost" onPress={navigateToHome} className="flex-1 items-center py-4">
          <Text className="text-blue-500 text-lg font-semibold">Home</Text>
        </Button>
        <Button variant="ghost" onPress={navigateToSearch} className="flex-1 items-center py-4">
          <Text className="text-blue-500 text-lg font-semibold">Search</Text>
        </Button>
        <Button variant="ghost" onPress={() => navigation.navigate('Transaction')} className="flex-1 items-center py-4">
          <Text className="text-blue-500 text-lg font-semibold">Transaction</Text>
        </Button>
      </HStack>
        </View>
        </VStack>
    );
};

export default SearchScreen;
