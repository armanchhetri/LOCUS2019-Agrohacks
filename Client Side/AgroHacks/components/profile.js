import React from 'react';
import { StyleSheet, Text, View, TouchableOpacity, ImageBackground, DrawerLayoutAndroid, Image, StatusBar } from 'react-native';
import {Container, Header, Icon, Left, Right, Body, Button, Card } from 'native-base';
import {User} from '../App';


export default class Profile extends React.Component {
    
  
    render() {
        var navigationView = (
            <View style={{flex: 1, backgroundColor: '#fff', marginTop:StatusBar.currentHeight}}>
              <Card style={{alignItems:'center', justifyContent:'center', height:150}}>
                <Image source={require('../assets/dp.jpg')} style={{height:120, width:120, borderRadius:60}} />
              </Card>
    
            </View>
        );
      return (
        
          <Container style= {styles.container}>
            <DrawerLayoutAndroid
                drawerWidth={250}
                drawerPosition={DrawerLayoutAndroid.positions.Right}
                renderNavigationView={() => navigationView}
            >

            <Header style={{justifyContent:'space-between', backgroundColor:'#0C9674', borderBottomWidth:1, borderBottomColor:'fff'}}>
                    <Left>
                    <TouchableOpacity onPress={() => this.props.navigation.openDrawer()}>
                        <Icon name="md-menu" style={{fontSize: 25, color: 'white'}} />
                    </TouchableOpacity>
                    </Left>
                    <Body >
                    <Text style={{fontSize:25, color:'white'}}>Profile</Text>
                    </Body>
                    <Right>
                    
                    </Right>
                </Header>
                <ImageBackground source={require('../assets/background.png')} style={{flex:1}}>
                
                <View style={{flex:1, alignItems:'center',justifyContent:'center'}}>
                    <TouchableOpacity activeOpacity={0.5}>
                        <Image source={require('../assets/dp.jpg')} style={[{height:120, width:120, borderRadius:60}, {shadowOpacity:1, shadowRadius:10} ]}  />
                    </TouchableOpacity>
                    <View style={{alignItems:'center'}}>
                        <Text style={{color:'white', fontSize:20}}>@manish</Text>
                    </View>
                    
                </View>
                <View style={{flex:1, flexDirection:'row', backgroundColor:'#0C9674'}}>
                    <View style={{flex:1}}>
                    
                    </View>

                    <View style={{flex:5, alignItems:'flex-start'}}>
                        <View style={{flexDirection:'row', paddingTop:20}}>
                            <Icon  name='md-menu' style={{height:20, color:'white',}} />
                            <Text style={{fontSize:20, color:'white', marginLeft:20}} >{User.name}</Text>

                        </View>
                        <View style={{flexDirection:'row', paddingTop:20}}>
                            <Icon  name='md-mail' style={{height:20, color:'white'}} />
                            <Text style={{fontSize:20, color:'white', marginLeft:20}}>9860687860</Text>

                        </View>
                        <View style={{flexDirection:'row', paddingTop:20}}>
                            <Icon  name='md-mail' style={{height:20, color:'white'}} />
                            <Text style={{fontSize:20, color:'white', marginLeft:20}}>manishdhakal521@gmail.com</Text>

                        </View>
                        
                    </View>
                </View>

                </ImageBackground>
            </DrawerLayoutAndroid>
          
          </Container>
      );
    } 
  }
  
  const styles = StyleSheet.create({
    container: {
      marginTop :  StatusBar.currentHeight,
      flex : 1,
      backgroundColor: 'white'
      
    }
  }); 