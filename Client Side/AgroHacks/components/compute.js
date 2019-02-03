import React from 'react';
import { StyleSheet, Text, View, TouchableOpacity, DrawerLayoutAndroid, StatusBar,Image } from 'react-native';
import {Container, Header, Icon, Left, Right, Body, Card, Button,  Content, Input, Label, Item, Form, Picker } from 'native-base';
//import {Drawer} from 'react-native-drawer';


export default class Home extends React.Component {
  constructor(props)
  {
    super(props);
    
  }
   
    render() {
      var navigationView = (
        <View style={{flex: 1, backgroundColor: '#fff', marginTop:StatusBar.currentHeight}}>
          <View style={{alignItems:'center', justifyContent:'center'}}>
            <Image source={require('../assets/dp.jpg')} style={{height:120, width:120, borderRadius:60}} />
          </View>
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
                    <TouchableOpacity onPress={() => this.props.navigation.openDrawer()}>
                    <Icon name="md-menu" style={{fontSize: 25, color: 'white'}} />
                    </TouchableOpacity>
                </Left>
                <Body >
                    <Text style={{fontSize:25, color:'white'}}>COMPUTE</Text>
                </Body>
                <Right>
                    <TouchableOpacity onPress={() => this.props.navigation.navigate('Profile')}>
                    <Image source={require('../assets/dp.jpg')} style={{height:30, width:30, borderRadius:15}} />
                    </TouchableOpacity>
                </Right>
                </Header>
                <Card>
                    <Form style={{padding:20}}>
                        <Item picker style={{ borderBottomWidth:1}}>
                        <Picker
                            mode="dropdown"
                            iosIcon={<Icon name="arrow-down" />}
                            style={{ width: undefined }}
                            placeholder="Select your Crop"
                            placeholderStyle={{ color: "#bfc6ea" }}
                            placeholderIconColor="#007aff"
                            // selectedValue={this.state.selected2}
                            // onValueChange={this.onValueChange2.bind(this)}
                        >
                            <Picker.Item label="Wheat" value="wheat" />
                            <Picker.Item label="Maize" value="maize" />
                            <Picker.Item label="Rice" value="rice" />
                            <Picker.Item label="Potato" value="potato" />
                            <Picker.Item label="Tomato" value="tomato" />
                        </Picker>
                        </Item>
                        <Item floatingLabel>
                            <Label>Param1</Label>
                            <Input />
                        </Item>
                        <Item style={{paddingBottom:10}} floatingLabel last>
                            <Label>Param2</Label>
                            <Input />
                        </Item>

                    </Form>

                    <Button block >
                        <Text style={{fontSize:18}}>Compute</Text>
                    </Button>
                </Card>
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