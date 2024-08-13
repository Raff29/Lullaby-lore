import React from 'react';
import { Box, Button, Container, Text, Heading } from '@chakra-ui/react';

const LandingSection = () => {
  return (
    <Container maxW="container.xl" className="text-center py-20">
      <Heading as="h1" size="2xl" className="text-blue-600">
        Welcome to Lullaby Lore
      </Heading>
      <Text fontSize="xl" className="mt-4 text-gray-600">
        Discover a collection of enchanting bedtime stories to read to your little ones.
      </Text>
      <Box mt="8">
        <Button colorScheme="blue" size="lg" className="mx-2">
          Explore Stories
        </Button>
        <Button colorScheme="teal" size="lg" className="mx-2">
          Learn More
        </Button>
      </Box>
    </Container>
  );
};

export default LandingSection;
