import React, { useState } from 'react';
import { View, TextInput, FlatList, Text } from 'react-native';
import { Box, Input, Icon } from 'native-base';
import { Ionicons } from '@expo/vector-icons';

const SearchScreen = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [results, setResults] = useState<string[]>([]);

    const handleSearch = (query: string) => {
        setSearchQuery(query);
        setResults(query ? ['Result 1', 'Result 2', 'Result 3'] : []);
    };

    return (
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
                keyExtractor={(item, index) => index.toString()}
                renderItem={({ item }) => (
                    <Box style={{ padding: 16, borderBottomWidth: 1, borderBottomColor: 'gray.200' }}>
                        <Text>{item}</Text>
                    </Box>
                )}
                ListEmptyComponent={<Text style={{ textAlign: 'center', color: 'gray.500' }}>No results found</Text>}
            />
        </View>
    );
};

export default SearchScreen;