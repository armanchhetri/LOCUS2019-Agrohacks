import React from 'react';
import Details from './components/details';
import Home from './components/home';
import Compute from './components/compute';
import Profile from './components/profile';
import Compute1 from './components/compute1';
import Compute2 from './components/compute2';


import {SafeAreaView, ScrollView, View, Image, StatusBar} from 'react-native';
import {createAppContainer, createDrawerNavigator, DrawerItems } from 'react-navigation';

const customDraw = (props) => (
  <SafeAreaView style={{flex:1, marginTop:StatusBar.currentHeight,}}>
    <View style={{height:150, flexDirection:'row', alignItems:'center', justifyContent:'center'}}>

      <Image source={require('./assets/logo.png')} style={{height:120, width:120, borderRadius:60, borderWidth:3, borderColor:'#01992c'}} />

    </View>
    <ScrollView>
      <DrawerItems {...props} />
    </ScrollView>
  </SafeAreaView>
)
 export default class App extends React.Component {

  render() {
    return (
      <Draw />
      
    );}
}

const Draw = createAppContainer(createDrawerNavigator({
  Home :{screen:Home} ,
  Details : {screen:Details},
  Compute: {screen:Compute},
  Profile: {screen:Profile},
  Compute1: {screen:Compute1},
  Compute2: {screen:Compute2},
},
{
  contentComponent: customDraw,
   
}));

export const User = {
  name:"Manish Dhakal",
  number : "9860687860"
} 
