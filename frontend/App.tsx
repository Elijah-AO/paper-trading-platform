import { NativeBaseProvider } from 'native-base';
import AppNavigator from './src/navigation/AppNavigator';

export default function App() {
  return (
    <NativeBaseProvider>
      <AppNavigator />
    </NativeBaseProvider>
  );
}
