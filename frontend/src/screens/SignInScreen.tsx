// src/screens/SignInScreen.tsx
import { useState } from 'react';
import { Box, Button, Center, FormControl, Heading, Input, VStack, Text, Pressable } from 'native-base';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../navigation/types'; // Import the types

type SignInScreenNavigationProp = StackNavigationProp<RootStackParamList, 'SignIn'>;

export default function SignInScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigation = useNavigation<SignInScreenNavigationProp>(); // Apply the type

const handleSignIn = async () => {
    try {
        const response = await fetch('http://localhost:5000/api/auth/signin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        const result = await response.json();

        if (response.ok) {
            console.log('User Signed in:', result.token);
            localStorage.setItem('token', result.token);
            navigation.navigate('Dashboard');
        } else {
            setError(result.error || 'Sign-in failed. Please try again.');
        }
    } catch (err) {
        console.error('Sign-in error:', err);
        setError('An error occurred. Please try again later.');
    }
};

  return (
    <Center flex={1} px={4} bg="white">
      <Box safeArea p="2" py="8" w="90%" maxW="290">
        <Heading size="lg" fontWeight="600" color="coolGray.800" _dark={{ color: 'warmGray.50' }}>
          Sign In
        </Heading>
        <VStack space={4} mt="5">
          <FormControl>
            <FormControl.Label>Email</FormControl.Label>
            <Input
              value={email}
              onChangeText={setEmail}
              placeholder="Enter your email"
            />
          </FormControl>
          <FormControl>
            <FormControl.Label>Password</FormControl.Label>
            <Input
              type="password"
              value={password}
              onChangeText={setPassword}
              placeholder="Enter your password"
            />
          </FormControl>
          <Button mt="2" colorScheme="blue" onPress={handleSignIn}>
            Sign In
          </Button>
          <Pressable onPress={() => navigation.navigate('SignUp')}>
            <Text mt="4" textAlign="center" color="coolGray.600" _dark={{ color: 'warmGray.200' }}>
              Don’t have an account? Sign Up
            </Text>
          </Pressable>
        </VStack>
      </Box>
    </Center>
  );
}
