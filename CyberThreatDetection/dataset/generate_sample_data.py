"""
Sample Dataset Generator
Generates a synthetic NSL-KDD-like network intrusion detection dataset
for training and demonstration purposes.
"""

import os
import numpy as np
import pandas as pd

np.random.seed(42)

NUM_SAMPLES = 25000

PROTOCOLS = ['tcp', 'udp', 'icmp']
SERVICES = [
    'http', 'smtp', 'ftp', 'ftp_data', 'ssh', 'telnet', 'dns',
    'pop3', 'imap', 'https', 'snmp', 'ntp', 'ldap', 'other'
]
FLAGS = ['SF', 'S0', 'REJ', 'RSTR', 'RSTO', 'SH', 'S1', 'S2', 'S3', 'OTH']

ATTACK_TYPES = {
    'normal': 0.45,
    'dos': 0.25,
    'probe': 0.15,
    'r2l': 0.10,
    'u2r': 0.05,
}

ATTACK_BINARY = {'normal': 0, 'dos': 1, 'probe': 1, 'r2l': 1, 'u2r': 1}


def generate_normal_traffic(n):
    """Generate features typical of normal network traffic."""
    return {
        'duration': np.random.exponential(scale=30, size=n).astype(int),
        'protocol_type': np.random.choice(['tcp', 'udp', 'icmp'], size=n, p=[0.7, 0.2, 0.1]),
        'service': np.random.choice(SERVICES, size=n, p=[0.3, 0.1, 0.08, 0.08, 0.08, 0.05, 0.05, 0.04, 0.04, 0.06, 0.03, 0.03, 0.03, 0.03]),
        'flag': np.random.choice(FLAGS, size=n, p=[0.7, 0.05, 0.05, 0.04, 0.04, 0.03, 0.03, 0.02, 0.02, 0.02]),
        'src_bytes': np.random.lognormal(mean=6, sigma=2, size=n).astype(int),
        'dst_bytes': np.random.lognormal(mean=7, sigma=2, size=n).astype(int),
        'land': np.zeros(n, dtype=int),
        'wrong_fragment': np.random.choice([0, 1, 2, 3], size=n, p=[0.95, 0.03, 0.01, 0.01]),
        'urgent': np.zeros(n, dtype=int),
        'hot': np.random.poisson(lam=0.3, size=n),
        'num_failed_logins': np.zeros(n, dtype=int),
        'logged_in': np.random.choice([0, 1], size=n, p=[0.2, 0.8]),
        'num_compromised': np.zeros(n, dtype=int),
        'root_shell': np.zeros(n, dtype=int),
        'su_attempted': np.zeros(n, dtype=int),
        'num_root': np.zeros(n, dtype=int),
        'num_file_creations': np.random.poisson(lam=0.1, size=n),
        'num_shells': np.zeros(n, dtype=int),
        'num_access_files': np.random.poisson(lam=0.05, size=n),
        'is_host_login': np.zeros(n, dtype=int),
        'is_guest_login': np.random.choice([0, 1], size=n, p=[0.95, 0.05]),
        'count': np.random.poisson(lam=10, size=n),
        'srv_count': np.random.poisson(lam=8, size=n),
        'serror_rate': np.random.beta(a=1, b=20, size=n).round(4),
        'srv_serror_rate': np.random.beta(a=1, b=20, size=n).round(4),
        'rerror_rate': np.random.beta(a=1, b=30, size=n).round(4),
        'srv_rerror_rate': np.random.beta(a=1, b=30, size=n).round(4),
        'same_srv_rate': np.random.beta(a=15, b=2, size=n).round(4),
        'diff_srv_rate': np.random.beta(a=1, b=15, size=n).round(4),
        'srv_diff_host_rate': np.random.beta(a=1, b=20, size=n).round(4),
        'dst_host_count': np.random.poisson(lam=100, size=n).clip(0, 255),
        'dst_host_srv_count': np.random.poisson(lam=80, size=n).clip(0, 255),
        'dst_host_same_srv_rate': np.random.beta(a=10, b=2, size=n).round(4),
        'dst_host_diff_srv_rate': np.random.beta(a=1, b=15, size=n).round(4),
        'dst_host_same_src_port_rate': np.random.beta(a=3, b=5, size=n).round(4),
        'dst_host_srv_diff_host_rate': np.random.beta(a=1, b=20, size=n).round(4),
        'dst_host_serror_rate': np.random.beta(a=1, b=20, size=n).round(4),
        'dst_host_srv_serror_rate': np.random.beta(a=1, b=20, size=n).round(4),
        'dst_host_rerror_rate': np.random.beta(a=1, b=30, size=n).round(4),
        'dst_host_srv_rerror_rate': np.random.beta(a=1, b=30, size=n).round(4),
    }


def generate_dos_traffic(n):
    """Generate features typical of Denial of Service attacks."""
    data = generate_normal_traffic(n)
    data['duration'] = np.random.choice([0, 1, 2], size=n, p=[0.7, 0.2, 0.1])
    data['src_bytes'] = np.random.lognormal(mean=3, sigma=1.5, size=n).astype(int)
    data['dst_bytes'] = np.random.choice([0, 1, 2], size=n, p=[0.6, 0.2, 0.2])
    data['count'] = np.random.poisson(lam=300, size=n).clip(0, 511)
    data['srv_count'] = np.random.poisson(lam=5, size=n)
    data['serror_rate'] = np.random.beta(a=10, b=2, size=n).round(4)
    data['srv_serror_rate'] = np.random.beta(a=10, b=2, size=n).round(4)
    data['same_srv_rate'] = np.random.beta(a=1, b=5, size=n).round(4)
    data['flag'] = np.random.choice(FLAGS, size=n, p=[0.1, 0.4, 0.15, 0.1, 0.1, 0.03, 0.03, 0.03, 0.03, 0.03])
    data['dst_host_serror_rate'] = np.random.beta(a=8, b=2, size=n).round(4)
    data['dst_host_srv_serror_rate'] = np.random.beta(a=8, b=2, size=n).round(4)
    data['logged_in'] = np.random.choice([0, 1], size=n, p=[0.85, 0.15])
    return data


def generate_probe_traffic(n):
    """Generate features typical of Probe/Scan attacks."""
    data = generate_normal_traffic(n)
    data['duration'] = np.random.choice([0, 1, 2, 3], size=n, p=[0.5, 0.2, 0.15, 0.15])
    data['count'] = np.random.poisson(lam=200, size=n).clip(0, 511)
    data['srv_count'] = np.random.poisson(lam=3, size=n)
    data['diff_srv_rate'] = np.random.beta(a=10, b=3, size=n).round(4)
    data['dst_host_diff_srv_rate'] = np.random.beta(a=8, b=3, size=n).round(4)
    data['dst_host_same_srv_rate'] = np.random.beta(a=2, b=8, size=n).round(4)
    data['rerror_rate'] = np.random.beta(a=5, b=3, size=n).round(4)
    data['flag'] = np.random.choice(FLAGS, size=n, p=[0.2, 0.15, 0.25, 0.1, 0.1, 0.05, 0.05, 0.03, 0.04, 0.03])
    data['logged_in'] = np.random.choice([0, 1], size=n, p=[0.7, 0.3])
    return data


def generate_r2l_traffic(n):
    """Generate features typical of Remote to Local attacks."""
    data = generate_normal_traffic(n)
    data['duration'] = np.random.exponential(scale=200, size=n).astype(int)
    data['num_failed_logins'] = np.random.poisson(lam=3, size=n)
    data['hot'] = np.random.poisson(lam=5, size=n)
    data['logged_in'] = np.random.choice([0, 1], size=n, p=[0.4, 0.6])
    data['num_compromised'] = np.random.poisson(lam=1, size=n)
    data['is_guest_login'] = np.random.choice([0, 1], size=n, p=[0.6, 0.4])
    data['service'] = np.random.choice(['ftp', 'telnet', 'smtp', 'pop3', 'imap', 'other'], size=n, p=[0.25, 0.25, 0.15, 0.1, 0.1, 0.15])
    return data


def generate_u2r_traffic(n):
    """Generate features typical of User to Root attacks."""
    data = generate_normal_traffic(n)
    data['duration'] = np.random.exponential(scale=100, size=n).astype(int)
    data['root_shell'] = np.random.choice([0, 1], size=n, p=[0.3, 0.7])
    data['su_attempted'] = np.random.choice([0, 1, 2], size=n, p=[0.4, 0.4, 0.2])
    data['num_root'] = np.random.poisson(lam=5, size=n)
    data['num_shells'] = np.random.poisson(lam=2, size=n)
    data['num_file_creations'] = np.random.poisson(lam=3, size=n)
    data['num_access_files'] = np.random.poisson(lam=4, size=n)
    data['logged_in'] = np.ones(n, dtype=int)
    data['hot'] = np.random.poisson(lam=10, size=n)
    return data


def generate_dataset(output_path=None):
    """Generate the complete synthetic intrusion detection dataset."""
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), 'network_intrusion_data.csv')

    frames = []
    generators = {
        'normal': generate_normal_traffic,
        'dos': generate_dos_traffic,
        'probe': generate_probe_traffic,
        'r2l': generate_r2l_traffic,
        'u2r': generate_u2r_traffic,
    }

    for label, fraction in ATTACK_TYPES.items():
        n = int(NUM_SAMPLES * fraction)
        data = generators[label](n)
        df = pd.DataFrame(data)
        df['attack_type'] = label
        df['label'] = ATTACK_BINARY[label]  # 0 = normal, 1 = attack
        frames.append(df)

    dataset = pd.concat(frames, ignore_index=True)
    dataset = dataset.sample(frac=1, random_state=42).reset_index(drop=True)

    dataset.to_csv(output_path, index=False)
    print(f"[+] Dataset generated: {output_path}")
    print(f"[+] Shape: {dataset.shape}")
    print(f"[+] Class distribution:")
    print(dataset['attack_type'].value_counts())
    print(f"\n[+] Binary label distribution:")
    print(dataset['label'].value_counts())

    return dataset


if __name__ == '__main__':
    generate_dataset()
