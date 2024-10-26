// src/screens/HomeScreen.tsx
import { Box, Button, Center, Heading, VStack } from 'native-base';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../navigation/types';

type HomeScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Home'>;

export default function HomeScreen() {
  const navigation = useNavigation<HomeScreenNavigationProp>();

  return (
    <Center flex={1} bg="white">
      <Box safeArea p="4" w="90%" maxW="300">
        <Heading size="lg" textAlign="center" mb="6">
          Welcome to Our App
        </Heading>
        <VStack space={4}>
          <Button colorScheme="blue" onPress={() => navigation.navigate('SignIn')}>
            Sign In
          </Button>
          <Button colorScheme="blue" variant="outline" onPress={() => navigation.navigate('SignUp')}>
            Sign Up
          </Button>
        </VStack>
      </Box>
    </Center>
  );
}
