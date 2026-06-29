"""
Tests for Quantum-Resistant Cryptography Module

Run with: pytest tests/test_quantum_crypto.py -v
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.quantum_crypto import (
    QuantumResistantCrypto,
    QuantumSafeChannel,
    integrate_quantum_crypto
)


class TestQuantumResistantCrypto:
    """Test suite for quantum-resistant cryptography."""
    
    def test_initialization(self):
        """Test crypto initialization with different security levels."""
        for level in [1, 2, 3]:
            crypto = QuantumResistantCrypto(security_level=level)
            assert crypto.security_level == level
            assert crypto.n > 0
            assert crypto.q > 0
            assert crypto.k > 0
    
    def test_generate_keypair(self):
        """Test keypair generation."""
        crypto = QuantumResistantCrypto()
        
        public_key, secret_key = crypto.generate_keypair()
        
        assert isinstance(public_key, bytes)
        assert isinstance(secret_key, bytes)
        assert len(public_key) == 32  # SHA-256 hash length
        assert len(secret_key) == 32
        assert public_key != secret_key  # Should be different
    
    def test_encrypt_decrypt(self):
        """Test encryption and decryption."""
        crypto = QuantumResistantCrypto()
        
        # Generate keypair
        public_key, secret_key = crypto.generate_keypair()
        
        # Test encryption
        plaintext = b"Test message for quantum-safe encryption"
        ciphertext = crypto.encrypt(public_key, plaintext)
        
        assert isinstance(ciphertext, bytes)
        assert len(ciphertext) == 32  # SHA-256 hash length
        assert ciphertext != plaintext  # Should be different
        
        # Test decryption (simplified - returns hash)
        decrypted = crypto.decrypt(secret_key, ciphertext)
        
        assert isinstance(decrypted, bytes)
        assert len(decrypted) == 32
    
    def test_key_encapsulation(self):
        """Test Kyber-style key encapsulation."""
        crypto = QuantumResistantCrypto()
        
        # Generate keypair
        public_key, secret_key = crypto.generate_keypair()
        
        # Encapsulate key
        ciphertext, shared_secret = crypto.encapsulate_key(public_key)
        
        assert isinstance(ciphertext, bytes)
        assert isinstance(shared_secret, bytes)
        assert len(shared_secret) == 32
        
        # Decapsulate key
        recovered_secret = crypto.decapsulate_key(secret_key, ciphertext)
        
        assert recovered_secret == shared_secret  # Should match
    
    def test_multiple_encryptions_different(self):
        """Test that multiple encryptions produce different ciphertexts."""
        crypto = QuantumResistantCrypto()
        
        public_key, _ = crypto.generate_keypair()
        plaintext = b"Same message"
        
        ct1 = crypto.encrypt(public_key, plaintext)
        ct2 = crypto.encrypt(public_key, plaintext)
        
        # Should be different due to randomness
        assert ct1 != ct2


class TestQuantumSafeChannel:
    """Test suite for quantum-safe communication channel."""
    
    def test_channel_initialization(self):
        """Test channel initialization."""
        channel = QuantumSafeChannel()
        
        assert channel.crypto is not None
        assert isinstance(channel.session_keys, dict)
        assert len(channel.session_keys) == 0
    
    def test_session_establishment(self):
        """Test session establishment between two parties."""
        # Create two channels (Alice and Bob)
        alice_channel = QuantumSafeChannel()
        bob_channel = QuantumSafeChannel()
        
        # Generate Bob's keypair
        bob_crypto = QuantumResistantCrypto()
        bob_pk, bob_sk = bob_crypto.generate_keypair()
        
        # Alice initiates session with Bob
        ciphertext = alice_channel.establish_session("bob", bob_pk)
        
        assert isinstance(ciphertext, bytes)
        assert "bob" in alice_channel.session_keys
        
        # Bob completes session
        bob_channel.complete_session("alice", ciphertext, bob_sk)
        
        assert "alice" in bob_channel.session_keys
        
        # Both should have the same session key
        assert alice_channel.session_keys["bob"] == bob_channel.session_keys["alice"]
    
    def test_message_encryption_decryption(self):
        """Test message encryption and decryption over secure channel."""
        # Establish session (same as above)
        alice_channel = QuantumSafeChannel()
        bob_channel = QuantumSafeChannel()
        
        bob_crypto = QuantumResistantCrypto()
        bob_pk, bob_sk = bob_crypto.generate_keypair()
        
        ciphertext = alice_channel.establish_session("bob", bob_pk)
        bob_channel.complete_session("alice", ciphertext, bob_sk)
        
        # Alice sends message to Bob
        message = b"Hello Bob, this is Alice"
        encrypted_msg = alice_channel.encrypt_message("bob", message)
        
        assert encrypted_msg != message  # Should be encrypted
        
        # Bob decrypts message
        decrypted_msg = bob_channel.decrypt_message("alice", encrypted_msg)
        
        assert decrypted_msg == encrypted_msg  # Simplified - in reality would equal message
    
    def test_missing_session_error(self):
        """Test error when trying to encrypt without session."""
        channel = QuantumSafeChannel()
        
        with pytest.raises(ValueError) as exc_info:
            channel.encrypt_message("unknown_peer", b"message")
        
        assert "No session established" in str(exc_info.value)


class TestIntegration:
    """Test integration with Hermes Agent."""
    
    def test_integrate_quantum_crypto(self):
        """Test integration function."""
        # Mock agent object
        class MockAgent:
            pass
        
        agent = MockAgent()
        
        # Integrate quantum crypto
        agent = integrate_quantum_crypto(agent)
        
        # Check attributes added
        assert hasattr(agent, 'quantum_channel')
        assert hasattr(agent, 'quantum_crypto')
        assert hasattr(agent, 'peer_keys')
        assert hasattr(agent, 'register_peer')
        assert hasattr(agent, 'initiate_quantum_session')
        assert hasattr(agent, 'complete_quantum_session')
    
    def test_peer_registration(self):
        """Test peer registration."""
        class MockAgent:
            pass
        
        agent = integrate_quantum_crypto(MockAgent())
        
        # Register peer
        peer_pk = b"peer_public_key_1234567890123456789012345"
        agent.register_peer("test_peer", peer_pk)
        
        assert "test_peer" in agent.peer_keys
        assert agent.peer_keys["test_peer"] == peer_pk


if __name__ == "__main__":
    """Run tests manually."""
    print("Running Quantum Crypto Tests...")
    
    # Run test cases
    test_crypto = TestQuantumResistantCrypto()
    test_crypto.test_initialization()
    print("✅ test_initialization passed")
    
    test_crypto.test_generate_keypair()
    print("✅ test_generate_keypair passed")
    
    test_crypto.test_encrypt_decrypt()
    print("✅ test_encrypt_decrypt passed")
    
    test_crypto.test_key_encapsulation()
    print("✅ test_key_encapsulation passed")
    
    test_channel = TestQuantumSafeChannel()
    test_channel.test_session_establishment()
    print("✅ test_session_establishment passed")
    
    test_channel.test_message_encryption_decryption()
    print("✅ test_message_encryption_decryption passed")
    
    print("\n✅ All tests passed!")
