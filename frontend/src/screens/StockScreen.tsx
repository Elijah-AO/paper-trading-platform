import React, { useEffect, useState } from 'react';
import { View, Text, Button, ActivityIndicator, Alert } from 'react-native';
import { useRoute, RouteProp } from '@react-navigation/native';
import { RootStackParamList } from '../navigation/types';

type StockScreenRouteProp = RouteProp<RootStackParamList, 'Stock'>;

const StockScreen = () => {
    const route = useRoute<StockScreenRouteProp>();
    const { stockId, symbol, name } = route.params;

    const [stockInfo, setStockInfo] = useState<any>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [ownsStock, setOwnsStock] = useState<boolean>(false);

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

    const handleSellStock = () => {
        Alert.alert("Sell Stock", `Selling stock: ${name}`);
        // Implement sell functionality here
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
                    <Button title="Buy" onPress={() => {/* Handle buy action */}} />
                    {ownsStock && (
                        <Button title="Sell" onPress={handleSellStock} color="red" />
                    )}
                </>
            )}
        </View>
    );
};

export default StockScreen;
