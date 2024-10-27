import React, { useEffect, useState } from 'react';
import { Alert, ActivityIndicator } from 'react-native';
import { View, Text, Button, Input, VStack, HStack, Center } from 'native-base';
import { useNavigation, NavigationProp } from '@react-navigation/native';
import { RootStackParamList } from '../navigation/types';

const TransactionScreen = () => {
    const [balance, setBalance] = useState<number | null>(null);
    const [amount, setAmount] = useState<string>(''); // Input for amount
    const [loading, setLoading] = useState<boolean>(true);
    const [userId, setUserId] = useState<string | null>(null); // Store user ID
    const navigation = useNavigation<NavigationProp<RootStackParamList>>();

    useEffect(() => {
        const fetchUserData = async () => {
            const token = localStorage.getItem('token');
            if (!token) {
                Alert.alert("Error", "No token found");
                setLoading(false);
                return;
            }

            try {
                const response = await fetch('http://localhost:5000/api/auth/me', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });
                if (response.ok) {
                    const userData = await response.json();
                    setBalance(userData.balance);
                    setUserId(String(userData.id)); // Save user ID
                    console.log("User Data:", userData);
                    console.log("User ID:", String(userData.id));
                    console.log("User id:", userId);
                } else {
                    const errorData = await response.json();
                    Alert.alert("Error", errorData.error || "Failed to fetch user data");
                }
            } catch (error) {
                console.error('Error fetching user data:', error);
                Alert.alert("Error", "An error occurred while fetching user data.");
            } finally {
                setLoading(false);
            }
        };

        fetchUserData();
    }, []);

    const handleTransaction = async (type: 'deposit' | 'withdraw') => {
        console.log("Handling transaction");
        const token = localStorage.getItem('token');
        if (!token) {
            console.log("No token found");
            Alert.alert("Error", "No token found");
            return;
        }
        
        if (!amount || isNaN(Number(amount)) || Number(amount) <= 0) {
            console.log("Invalid input");
            Alert.alert("Invalid Input", "Please enter a valid positive number.");
            return;
        }

        if (!userId) {
            console.log("User ID not available");
            Alert.alert("Error", "User ID not available");
            return;
        }

        try {
            console.log(`Attempting ${type} of $${amount} for user ${userId}`);
            const response = await fetch(`http://localhost:5000/api/transactions/${type}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ amount: Number(amount), user_id: userId }),
            });
            
            if (response.ok) {
                Alert.alert("Success", `${type === 'deposit' ? 'Deposit' : 'Withdrawal'} successful`);
                setAmount(''); // Clear input
                const updatedBalance = await response.json();
                setBalance(updatedBalance.balance);
                navigation.navigate('Dashboard');
            } else {
                const errorData = await response.json();
                Alert.alert("Error", errorData.error || "Transaction failed");
            }
        } catch (error) {
            console.error(`Error on ${type}:`, error);
            Alert.alert("Error", "An error occurred during the transaction.");
        }
    };

    if (loading) {
        return (
            <Center flex={1}>
                <ActivityIndicator size="large" color="#0000ff" />
            </Center>
        );
    }

    return (
        <View className="flex-1 bg-white p-4">
            <VStack space={4} className="items-center">
                <Text className="text-2xl font-bold">Balance: ${balance?.toFixed(2)}</Text>
                
                <Input
                    placeholder="Enter amount"
                    keyboardType="numeric"
                    value={amount}
                    onChangeText={setAmount}
                    className="w-4/5 border border-gray-300 rounded-md px-3 py-2"
                />

                <HStack space={2} className="w-4/5 mt-4">
                    <Button flex={1} colorScheme="blue" onPress={() => {console.log("pressed");handleTransaction('deposit');console.log("left");}}>
                        Deposit
                    </Button>
                    <Button flex={1} colorScheme="red" onPress={() => handleTransaction('withdraw')}>
                        Withdraw
                    </Button>
                </HStack>
            </VStack>
        </View>
    );
};

export default TransactionScreen;
