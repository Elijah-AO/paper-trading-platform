// src/navigation/types.ts
export type RootStackParamList = {
    Home: undefined;
    SignIn: undefined;
    SignUp: undefined;
    Dashboard: undefined;
    Search: undefined;
    Stock: { stockId: string; symbol: string; name: string };
    Transaction: undefined;
  };
  