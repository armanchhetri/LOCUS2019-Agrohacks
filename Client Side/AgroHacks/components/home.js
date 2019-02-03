import React from 'react';
import { StyleSheet, Text, View, TouchableOpacity, DrawerLayoutAndroid, StatusBar,Image } from 'react-native';
import {Container, Header, Icon, Left, Right, Body, Button, Card, Content } from 'native-base';
//import {Drawer} from 'react-native-drawer';


export default class Home extends React.Component {
  constructor(props)
  {
    super(props);

    
  }

   
   
    render() {
      var ty= () => {
         this.props.navigation.openDrawer();
      }
      
      var navigationView = (
        <View style={{flex: 1, backgroundColor: '#fff', marginTop:StatusBar.currentHeight}}>
          <Card style={{alignItems:'center', justifyContent:'center', height:150}}>
            <Image source={require('../assets/dp.jpg')} style={{height:120, width:120, borderRadius:60}} />
          </Card>

        </View>
      );
      return (
        <Container style={styles.container}>
          <DrawerLayoutAndroid
            drawerWidth={250}
            drawerPosition={DrawerLayoutAndroid.positions.Right}
            renderNavigationView={() => navigationView}>
              <Header style={{justifyContent:'space-between', backgroundColor:'#0C9674'}}>
                <Left>
                  <TouchableOpacity onPress={ty}>
                    <Icon name="md-menu" style={{fontSize: 25, color: 'white'}} />
                  </TouchableOpacity>
                </Left>
                <Body >
                  <Text style={{fontSize:25, color:'white'}}>AgroHacks</Text>
                </Body>
                <Right>
                  <TouchableOpacity onPress={() => this.props.navigation.navigate('Profile')}>
                    <Image source={require('../assets/dp.jpg')} style={{height:30, width:30, borderRadius:15}} />
                  </TouchableOpacity>
                </Right>
              </Header>

              <View style={{flex:1}}>
                <Card style={{flex:1}}>
                  <View style={{marginHorizontal:10, borderBottomWidth:1}}>
                    <Text style={{fontSize:20, fontWeight:'bold'}}>Resources Allocated</Text>
                  </View>

                  <View style={{flexDirection:'row', marginHorizontal:10,}}>

                    <View style={{flex:1, borderBottomWidth:1}}>
                      <Text style={{fontSize:20,}} >Crops</Text>
                    </View>

                    <View style={{flex:1, borderBottomWidth:1}}>
                      <Text style={{fontSize:20,}} >Qty</Text>
                      
                    </View>

                    <View style={{ flex:1, borderBottomWidth:1}}>
                    <Text style={{fontSize:20,}}>Region</Text>
                      
                    </View>

                  </View>

                </Card>

                <Card style={{flex:1}}>
                  

                </Card>


                <View style={{flex:1, flexDirection:'row'}}>
                  <Card style={{flex:1}}>
                
                  </Card>
                  <Card style={{flex:1}}>

                  </Card>
                
                </View>

              </View>

          </DrawerLayoutAndroid>
        </Container>


      );
    } 
  }
  
  const styles = StyleSheet.create({
    container: {
      marginTop: StatusBar.currentHeight,
      flex : 1,
      backgroundColor: '#ccc'
      
    }
  }); 