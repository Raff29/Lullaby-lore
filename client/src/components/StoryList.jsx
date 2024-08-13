import React from 'react';
import { Box, Container, Text } from '@chakra-ui/react';

const stories = [
  { title: 'The Little Star', description: 'A story about a star finding its place in the sky.' },
  { title: 'The Brave Knight', description: 'A knight who overcomes challenges with courage.' },
  { title: 'The Whispering Trees', description: 'Trees that tell tales of ancient times.' },
];

const StoryList = () => {
  return (
    <Container maxW="container.md" className="my-8">
      {stories.map((story, index) => (
        <Box
          key={index}
          bg="white"
          shadow="md"
          rounded="lg"
          p="6"
          mb="6"
          _hover={{ bg: 'blue.50' }}
        >
          <Text fontSize="xl" fontWeight="bold">
            {story.title}
          </Text>
          <Text mt="2">{story.description}</Text>
        </Box>
      ))}
    </Container>
  );
};

export default StoryList;
