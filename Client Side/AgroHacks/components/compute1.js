import React from 'react';
import { StyleSheet, Text, View, TouchableOpacity, StatusBar } from 'react-native';
import {Container, Header, Icon, Left, Right, Body, Button, Card } from 'native-base';


export default class Compute1 extends React.Component {

  constructor(props){
    super(props);
    this.state ={
      clicked:false
    }

    this.content = null;

    this.click = this.click.bind(this);
  }

  click(){
    this.state.clicked = true;
         
        
    
  }

    render() {
      let dar = <View><Text>manish</Text></View>

      return (
        
          <Container style= {styles.container}>
          <Header></Header>
          <TouchableOpacity onPress={this.click }>
            <Text> this is compute1 </Text>
          </TouchableOpacity>
            {dar}
           
          </Container>
      );
    } 
  }
  
  const styles = StyleSheet.create({
    container: {
      marginTop : StatusBar.currentHeight,
      flex : 1,
      backgroundColor: 'white',
      alignItems : 'center',
      justifyContent :'center'
      
    }
  }); 