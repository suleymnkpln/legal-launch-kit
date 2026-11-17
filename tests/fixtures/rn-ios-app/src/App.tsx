import auth from '@react-native-firebase/auth';
import Purchases from 'react-native-purchases';
import mobileAds from 'react-native-google-mobile-ads';
import OpenAI from 'openai';

export async function signUp(email: string, password: string) {
  return auth().createUserWithEmailAndPassword(email, password);
}

export async function deleteAccount() {
  await auth().currentUser?.delete();
}

export async function buyPremium() {
  // monthly plan, auto-renew
  return Purchases.purchasePackage(pkg);
}
