import React, { createContext, useState, useContext, ReactNode } from 'react';

// Create a TimerContext to manage the `length` state
const TimerContext = createContext<{
  length: number;
  setLength: React.Dispatch<React.SetStateAction<number>>;
}>({
  length: 0, // default length is 0
  setLength: () => {},
});

// Custom hook to access TimerContext
export const useTimer = () => useContext(TimerContext);

// TimerProvider component to wrap the app with TimerContext
interface TimerProviderProps {
  children: ReactNode;
}

export const TimerProvider: React.FC<TimerProviderProps> = ({ children }) => {
  const [length, setLength] = useState<number>(0); // Initialize with 0

  return (
    <TimerContext.Provider value={{ length, setLength }}>
      {children}
    </TimerContext.Provider>
  );
};
