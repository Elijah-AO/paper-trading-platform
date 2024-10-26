// src/screens/SignUpScreen.tsx
import { useState } from 'react';
import { View, Text } from 'react-native';
import InputField from '../components/InputField';
import Button from '../components/Button';

export default function SignUpScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignUp = () => {
    // Logic for handling sign-up, e.g., API call
    console.log('Signing up with:', email, password);
  };

  return (
    <View className="flex-1 bg-white justify-center p-6">
      <Text className="text-2xl font-bold text-center mb-6">Sign Up</Text>
      <InputField placeholder="Email" onChangeText={setEmail} />
      <InputField placeholder="Password" secureTextEntry onChangeText={setPassword} />
      <Button title="Sign Up" onPress={handleSignUp} />
    </View>
  );
}
