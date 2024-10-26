// src/screens/DashboardScreen.tsx
import React, { useEffect, useState } from 'react';
import { View, Text, Alert } from 'react-native';
import { ScrollView } from 'native-base';
import TradingCard from '../components/TradingCard';
type Stock = {
  _id: string;
  name: string;
  quantity: number;
};

export default function DashboardScreen() {
  const [balance, setBalance] = useState(0);
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchDashboardData = async () => {
      const token = localStorage.getItem('token'); // Retrieve token from local storage

      try {
        const response = await fetch('http://localhost:5000/api/users/dashboard', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
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

    fetchDashboardData();
  }, []);

  const handleCardPress = (stockName: string) => {
    Alert.alert("Stock Selected", `You selected ${stockName}`);
  };

  return (
    <View style={{ flex: 1, alignItems: 'center', backgroundColor: '#fff', paddingTop: 20 }}>
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
                  onPress={() => handleCardPress(stock.name)}
                />
              ))
            ) : (
              <Text style={{ color: 'gray' }}>No stocks available</Text>
            )}
          </ScrollView>
        </>
      )}
    </View>
  );
}
