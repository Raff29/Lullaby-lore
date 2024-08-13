import React from 'react';
import { Box, Text } from '@chakra-ui/react';

const Footer = () => {
  return (
    <Box bg="blue.500" color="white" py="4" mt="8">
      <Text textAlign="center">
        © {new Date().getFullYear()} Lullaby Lore. All rights reserved.
      </Text>
    </Box>
  );
};

export default Footer;
