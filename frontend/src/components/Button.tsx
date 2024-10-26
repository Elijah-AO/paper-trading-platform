// src/components/Button.tsx
import { Text, TouchableOpacity } from 'react-native';

interface ButtonProps {
  title: string;
  onPress: () => void;
}

export default function Button({ title, onPress }: ButtonProps) {
  return (
    <TouchableOpacity onPress={onPress} className="bg-blue-500 rounded-lg p-3">
      <Text className="text-white text-center text-lg">{title}</Text>
    </TouchableOpacity>
  );
}
