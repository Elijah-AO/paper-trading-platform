import { useState } from 'react';
import { Box, Button, Center, FormControl, Heading, Input, VStack, Text, Pressable, Alert } from 'native-base';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../navigation/types';

type SignUpScreenNavigationProp = StackNavigationProp<RootStackParamList, 'SignUp'>;

export default function SignUpScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigation = useNavigation<SignUpScreenNavigationProp>();

  const handleSignUp = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const result = await response.json();

      if (response.ok) {
        console.log('User registered:', result.user_id);
        navigation.navigate('Home');
      } else {
        setError(result.error || 'Sign-up failed. Please try again.');
      }
    } catch (err) {
      console.error('Sign-up error:', err);
      setError('An error occurred. Please try again later.');
    }
  };

  return (
    <Center flex={1} px={4} bg="white">
      <Box safeArea p="2" py="8" w="90%" maxW="290">
        <Heading size="lg" fontWeight="600" color="coolGray.800">
          Sign Up
        </Heading>
        <VStack space={4} mt="5">
          {error && <Alert status="error">{error}</Alert>}
          <FormControl>
            <FormControl.Label>Email</FormControl.Label>
            <Input value={email} onChangeText={setEmail} placeholder="Enter your email" />
          </FormControl>
          <FormControl>
            <FormControl.Label>Password</FormControl.Label>
            <Input type="password" value={password} onChangeText={setPassword} placeholder="Enter your password" />
          </FormControl>
          <Button mt="2" colorScheme="blue" onPress={handleSignUp}>
            Sign Up
          </Button>
          <Pressable onPress={() => navigation.navigate('SignIn')}>
            <Text mt="4" textAlign="center" color="coolGray.600">
              Already have an account? Sign In
            </Text>
          </Pressable>
        </VStack>
      </Box>
    </Center>
  );
}
