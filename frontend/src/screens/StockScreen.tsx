import React, { useEffect, useState } from 'react';
import { View, Text, Button, ActivityIndicator, Alert, TextInput } from 'react-native';
import { useRoute, RouteProp, useNavigation } from '@react-navigation/native';
import { RootStackParamList } from '../navigation/types';
import { NavigationProp } from '@react-navigation/native';

type StockScreenRouteProp = RouteProp<RootStackParamList, 'Stock'>;

const StockScreen = () => {
    const route = useRoute<StockScreenRouteProp>();
    const { stockId, symbol, name } = route.params;
    const navigation = useNavigation<NavigationProp<RootStackParamList>>();
    const [userId, setUserId] = useState<string | null>(null);
    const [stockInfo, setStockInfo] = useState<any>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [ownsStock, setOwnsStock] = useState<boolean>(false);
    const [quantity, setQuantity] = useState<string>(''); // Input field for quantity

    useEffect(() => {
        const fetchStockInfoAndUserData = async () => {
            const token = localStorage.getItem('token');
            if (!token) {
                console.error("No token found");
                setLoading(false);
                return;
            }

            try {
                // Fetch stock information
                const stockResponse = await fetch(`http://localhost:5000/api/stocks/${stockId}`);
                const stockData = await stockResponse.json();
                setStockInfo(stockData);

                // Fetch user information using the /me route
                const userResponse = await fetch('http://localhost:5000/api/auth/me', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });

                if (userResponse.ok) {
                    const userData = await userResponse.json();
                    const userStocks = userData.stocks || {};
                    setOwnsStock(userStocks.hasOwnProperty(stockId));
                    setUserId(userData.id);
                } else {
                    console.error('Failed to fetch user data');
                }
            } catch (error) {
                console.error('Error fetching stock info or user data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchStockInfoAndUserData();
    }, [stockId]);

    const handleTrade = async (type: 'buy' | 'sell') => {
        const token = localStorage.getItem('token');
        if (!token) {
            Alert.alert("Error", "No token found");
            return;
        }

        if (!quantity || isNaN(Number(quantity)) || Number(quantity) <= 0) {
            Alert.alert("Invalid Input", "Please enter a valid quantity.");
            return;
        }

        try {
            const response = await fetch(`http://localhost:5000/api/trades/${type}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ stock_id: stockId, quantity: Number(quantity), user_id: userId }),
            });

            if (response.ok) {
                Alert.alert("Success", `${type === 'buy' ? 'Purchase' : 'Sale'} successful`);
                setQuantity(''); // Clear the input field
                navigation.navigate('Dashboard'); // Go back to the Dashboard to refresh data
            } else {
                const errorData = await response.json();
                Alert.alert("Error", errorData.error || `${type === 'buy' ? 'Purchase' : 'Sale'} failed`);
            }
        } catch (error) {
            console.error(`Error on ${type}:`, error);
            Alert.alert("Error", "An error occurred during the transaction.");
        }
    };

    if (loading) {
        return (
            <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
                <ActivityIndicator size="large" color="#0000ff" />
            </View>
        );
    }

    return (
        <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center', padding: 16 }}>
            <Text style={{ fontSize: 24, fontWeight: 'bold' }}>{symbol}</Text>
            <Text style={{ fontSize: 18, color: 'gray' }}>{name}</Text>
            <Text style={{ marginTop: 20 }}>Stock ID: {stockId}</Text>
            {stockInfo && (
                <>
                    <Text style={{ marginTop: 20 }}>Price: {stockInfo.price}</Text>
                    <Text>Last Updated: {stockInfo.date_updated}</Text>

                    <TextInput
                        style={{
                            borderWidth: 1,
                            borderColor: '#ccc',
                            borderRadius: 5,
                            padding: 8,
                            marginTop: 20,
                            width: '80%',
                        }}
                        placeholder="Enter quantity"
                        keyboardType="numeric"
                        value={quantity}
                        onChangeText={setQuantity}
                    />

                    <Button title="Buy" onPress={() => handleTrade('buy')} />
                    {ownsStock && (
                        <Button title="Sell" onPress={() => handleTrade('sell')} color="red" />
                    )}
                </>
            )}
        </View>
    );
};

export default StockScreen;
