const tableConfigs = {
    'users': {
        endpoint: '/users',
        title: 'Users',
        fields: [
            { name: 'user_id', label: 'User ID', type: 'number', readonly: true },
            { name: 'email', label: 'Email', type: 'email', required: true },
            { name: 'given_name', label: 'Given Name', type: 'text', required: true },
            { name: 'surname', label: 'Surname', type: 'text', required: true },
            { name: 'city', label: 'City', type: 'text', required: true },
            { name: 'phone_number', label: 'Phone Number', type: 'text', required: true },
            { name: 'profile_description', label: 'Profile Description', type: 'textarea' },
            { name: 'password', label: 'Password', type: 'text', required: true }
        ],
        idField: 'user_id'
    },
    'caregivers': {
        endpoint: '/caregivers',
        title: 'Caregivers',
        fields: [
            { name: 'caregiver_user_id', label: 'Caregiver User ID', type: 'number', required: true },
            { name: 'gender', label: 'Gender', type: 'select', options: ['MALE', 'FEMALE', 'OTHER'], required: true },
            { name: 'caregiving_type', label: 'Caregiving Type', type: 'select', options: ['BABYSITTER', 'ELDERLY_CARE', 'PLAYMATE_FOR_CHILDREN'], required: true },
            { name: 'hourly_rate', label: 'Hourly Rate', type: 'number', required: true },
            { name: 'photo', label: 'Photo', type: 'file', required: true, optionalInUpdate: true }
        ],
        idField: 'caregiver_user_id'
    },
    'members': {
        endpoint: '/members',
        title: 'Members',
        fields: [
            { name: 'member_user_id', label: 'Member User ID', type: 'number', required: true },
            { name: 'house_rules', label: 'House Rules', type: 'textarea' },
            { name: 'dependent_description', label: 'Dependent Description', type: 'textarea' }
        ],
        idField: 'member_user_id'
    },
    'addresses': {
        endpoint: '/addresses',
        title: 'Addresses',
        fields: [
            { name: 'member_user_id', label: 'Member User ID', type: 'number', required: true },
            { name: 'house_number', label: 'House Number', type: 'text', required: true },
            { name: 'street', label: 'Street', type: 'text', required: true },
            { name: 'town', label: 'Town', type: 'text', required: true }
        ],
        idField: 'member_user_id'
    },
    'jobs': {
        endpoint: '/jobs',
        title: 'Jobs',
        fields: [
            { name: 'job_id', label: 'Job ID', type: 'number', readonly: true },
            { name: 'member_user_id', label: 'Member User ID', type: 'number', required: true },
            { name: 'required_caregiving_type', label: 'Required Caregiving Type', type: 'select', options: ['BABYSITTER', 'ELDERLY_CARE', 'PLAYMATE_FOR_CHILDREN'], required: true },
            { name: 'other_requirements', label: 'Other Requirements', type: 'textarea' },
            { name: 'date_posted', label: 'Date Posted', type: 'date' }
        ],
        idField: 'job_id'
    },
    'job-applications': {
        endpoint: '/job-applications',
        title: 'Job Applications',
        fields: [
            { name: 'caregiver_user_id', label: 'Caregiver User ID', type: 'number', required: true },
            { name: 'job_id', label: 'Job ID', type: 'number', required: true },
            { name: 'date_applied', label: 'Date Applied', type: 'date' }
        ],
        idField: null,
        compositeKey: ['caregiver_user_id', 'job_id']
    },
    'appointments': {
        endpoint: '/appointments',
        title: 'Appointments',
        fields: [
            { name: 'appointment_id', label: 'Appointment ID', type: 'number', readonly: true },
            { name: 'caregiver_user_id', label: 'Caregiver User ID', type: 'number', required: true },
            { name: 'member_user_id', label: 'Member User ID', type: 'number', required: true },
            { name: 'appointment_date', label: 'Appointment Date', type: 'date', required: true },
            { name: 'appointment_time', label: 'Appointment Time', type: 'time', required: true },
            { name: 'work_hours', label: 'Work Hours', type: 'number', required: true },
            { name: 'status', label: 'Status', type: 'select', options: ['PENDING', 'ACCEPTED', 'DECLINED'], required: true }
        ],
        idField: 'appointment_id'
    }
};

