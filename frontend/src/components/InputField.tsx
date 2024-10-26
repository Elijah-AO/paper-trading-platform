// src/components/InputField.tsx
import { TextInput, View } from 'react-native';

interface InputFieldProps {
  placeholder: string;
  secureTextEntry?: boolean;
  onChangeText: (text: string) => void;
}

export default function InputField({ placeholder, secureTextEntry, onChangeText }: InputFieldProps) {
  return (
    <View className="mb-4">
      <TextInput
        placeholder={placeholder}
        secureTextEntry={secureTextEntry}
        onChangeText={onChangeText}
        className="border border-gray-300 rounded-lg p-2 text-lg"
      />
    </View>
  );
}
