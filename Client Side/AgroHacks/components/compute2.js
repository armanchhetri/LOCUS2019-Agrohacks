import React from 'react';
import { StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import {Container, Header, Icon, Left, Right, Body, Button, Card } from 'native-base';




export default class Compute2 extends React.Component {
  
    render() {
      return (
        
          <Container style= {styles.container}>
           <Text> this is compute2 </Text> 
          </Container>
      );
    } 
  }
  
  const styles = StyleSheet.create({
    container: {
      marginTop : Expo.Constants.statusBarHeight,
      flex : 1,
      backgroundColor: 'white'
      
    }
  }); 