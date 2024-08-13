import React from 'react';
import Header from './components/Header';
import LandingSection from './components/LandingSection';
import Footer from './components/Footer';
import { ChakraProvider } from '@chakra-ui/react';

function App() {
  return (
    <ChakraProvider>
      <div className="flex flex-col min-h-screen bg-gray-100">
        <Header />
        <main className="flex-grow">
          <LandingSection />
        </main>
        <Footer />
      </div>
    </ChakraProvider>
  );
}

export default App;
