import React, { useEffect, useState } from 'react';
import { View, Text } from 'react-native';
import { ScrollView, VStack, HStack, Button } from 'native-base';
import TradingCard from '../components/TradingCard';
import { useNavigation, useFocusEffect } from '@react-navigation/native';
import { RootStackParamList } from '../navigation/types';
import { NavigationProp } from '@react-navigation/native';

type Stock = {
  _id: string;
  name: string;
  quantity: number;
};

export default function DashboardScreen() {
  const [balance, setBalance] = useState(0);
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [error, setError] = useState('');
  const navigation = useNavigation<NavigationProp<RootStackParamList>>();

  const fetchDashboardData = async () => {
    const token = localStorage.getItem('token'); // Retrieve token from local storage

    try {
      const response = await fetch('http://localhost:5000/api/users/dashboard', {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setBalance(data.balance);
        setStocks(data.stocks); // Assuming data.stocks is an array of Stock
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Failed to fetch data');
      }
    } catch (error) {
      setError('An error occurred. Please try again.');
    }
  };

  useEffect(() => {
    // Add focus listener to refresh data each time screen is focused
    const unsubscribe = navigation.addListener('focus', fetchDashboardData);

    // Cleanup the listener on component unmount
    return unsubscribe;
  }, [navigation]);

  const handleCardPress = (stock: Stock) => {
    navigation.navigate('Stock', {
      stockId: stock._id,
      symbol: stock.name,
      name: stock.name,
    });
  };

  return (
    <VStack className="flex-1 bg-white">
      <View style={{ flex: 1, alignItems: 'center', paddingTop: 20 }}>
        {error ? (
          <Text style={{ color: 'red' }}>{error}</Text>
        ) : (
          <>
            <Text style={{ fontSize: 24, fontWeight: 'bold' }}>Balance: ${balance.toFixed(2)}</Text>
            <Text style={{ fontSize: 20, fontWeight: '600', marginTop: 16 }}>Stocks:</Text>
            <ScrollView contentContainerStyle={{ alignItems: 'center', paddingVertical: 10 }}>
              {stocks.length ? (
                stocks.map((stock) => (
                  <TradingCard
                    key={stock._id}
                    stockName={stock.name}
                    stockId={stock._id}
                    quantity={stock.quantity}
                    onPress={() => handleCardPress(stock)}
                  />
                ))
              ) : (
                <Text style={{ color: 'gray' }}>No stocks available</Text>
              )}
            </ScrollView>
          </>
        )}
      </View>

      <HStack className="border-t border-gray-300 bg-gray-100" style={{ width: '100%' }}>
        <Button variant="ghost" onPress={() => navigation.navigate('Dashboard')} className="flex-1 items-center py-4">
          <Text className="text-blue-500 text-lg font-semibold">Home</Text>
        </Button>
        <Button variant="ghost" onPress={() => navigation.navigate('Search')} className="flex-1 items-center py-4">
          <Text className="text-blue-500 text-lg font-semibold">Search</Text>
        </Button>
        <Button variant="ghost" onPress={() => navigation.navigate('Transaction')} className="flex-1 items-center py-4">
          <Text className="text-blue-500 text-lg font-semibold">Transaction</Text>
        </Button>
      </HStack>
    </VStack>
  );
}
